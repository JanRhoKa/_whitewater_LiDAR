import numpy as np
import pandas as pd

from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from scipy.interpolate import splrep, splev


def bathy_convolution(time_intervals, amplitude_param, mu, sigma, extinction_coefficient):
    """
        Convolution of the Gaussian pulse and an exponential function to simulate the interaction of LiDAR and water
    """

    return np.convolve(amplitude_param * np.exp(-(time_intervals-mu)**2/(2*sigma**2)),  
                       np.exp(-extinction_coefficient * time_intervals), mode="same")




def fit_curve_whitewater(x_optimize, y_optimize):
    """
        Fits the bathy convolution to the current waveform.
    """

    # interpolate wfm to have length 400
    spline_param = splrep(x=x_optimize, y=y_optimize, s=0)
    x_optimize = np.arange(min(x_optimize), max(x_optimize), (max(x_optimize)- min(x_optimize))/1000)

    # get start of wfm
    wfm_start = x_optimize[0]

    # adjust interpolation to start at 0
    y_optimize = splev(x_optimize, spline_param)
    x_optimize = x_optimize - wfm_start

    # scipy curve fit
    popt, _ = curve_fit(bathy_convolution, x_optimize, y_optimize, maxfev=250)
    
    return x_optimize + wfm_start, y_optimize, bathy_convolution(x_optimize, *popt)


def extract_second_echo(white_water_wfm):
    """
        Gets second echo for whitewater waveform by subtracting water column backscatter.
    """

    # get wfm data (time, amplitude)
    x_values_white_water = white_water_wfm[0]
    y_values_white_water = white_water_wfm[1]

    # try fitting if not return [0]
    try:
        # get white water simulation 
        interpolated_time, interpolated_wfm, wfm_white_water = fit_curve_whitewater(x_values_white_water, y_values_white_water)

        # difference peak between simulation and wfm
        differences_measured_simulation = interpolated_wfm - wfm_white_water
        max_differences = find_peaks(differences_measured_simulation, distance=250)

        # new postion as interpolated SI
        position_time_second_peak = np.array([interpolated_time[peak] for peak in max_differences[0]])
        
    except:
        position_time_second_peak = [0]


    return position_time_second_peak


def extract_new_whitwater_points(lidar_df, waveform_data_recorded, socs_coordinates, direction_vector, sample_intervals, range_gate_whitewater=1, n_refrac=1.335):
    """
        Extract the whitewater points as described in https://doi.org/10.1002/rra.70109%20.
    """

    # speed of light [m/s]
    c = 299792458

    # point cloud data
    nr_of_echoes = lidar_df["nr_of_echos"].values
    coordinates = lidar_df[["x", "y", "z"]].values

    # wfm offsets [ns]
    time_to_wfm = lidar_df["wfm_time_offset"].values
    ampl_to_wfm = lidar_df["wfm_ampl_offset"].values

    new_points_list = []
    for i, wfm in enumerate(waveform_data_recorded):
        
        # transpose wfm from samples
        wfm = wfm.T

        # waveform can only have one echo and waveform data must be recorded
        if nr_of_echoes[i] < 2 and len(wfm) > 1 and len(wfm[0]) > 1:
            
            # peak position whitewater from beginning wfm [SI]
            new_peak_positions = extract_second_echo(wfm)

            # 
            if len(new_peak_positions) > 0:
                if new_peak_positions[0] != 0 and len(new_peak_positions) >= range_gate_whitewater + 1:

                    # distance scanner [m]
                    distance_anchor_scanner = np.linalg.norm(socs_coordinates[i])
                        
                    # transform time to ns [ns]
                    new_peak = new_peak_positions[range_gate_whitewater] * sample_intervals

                    # distance of new echo from scanner [m]
                    total_distance_new_point = (new_peak + time_to_wfm[i] + ampl_to_wfm[i]) * c/2
                        
                    # calculate distance between existing point and new point, apply refraction correction [m]
                    point_movement = (total_distance_new_point - distance_anchor_scanner)/n_refrac * direction_vector[i]

                    # get new point coordinates
                    new_point = coordinates[i] + point_movement

                    # filter point if new point is to close to the water surface (bad curve fitting)
                    if distance_anchor_scanner + 0.205 < total_distance_new_point:
                        new_points_list.append(new_point)

    # add all new points to a dataframe
    new_points_df = pd.DataFrame({"x": np.array(new_points_list).T[0], "y": np.array(new_points_list).T[1], "z": np.array(new_points_list).T[2]})

    return new_points_df