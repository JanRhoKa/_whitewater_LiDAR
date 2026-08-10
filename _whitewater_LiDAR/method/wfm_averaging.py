import numpy as np
import pandas as pd

from scipy.interpolate import splrep, splev


def wfm_averaging_function(wfm_data):
    """
        Averages the given waveforms into a single interpolated (higher sampled) waveform.
    """

    # initiates lists for data collection
    corrected_time, amplitude_wfms = [], []

    for wfm in wfm_data:

        # get wfm data
        time, amplitude = wfm.T[0], wfm.T[1]

        # transform data to same scale
        amplitude_wfms.extend(amplitude)
        corrected_time.extend((time - time[0]) * 5.0251272613070636e-10 * 1e9)
    
    # convert to array
    corrected_time = np.array(corrected_time)
    amplitude_wfms = np.array(amplitude_wfms)

    # create a df for the wfm averaging
    df_plot = pd.DataFrame()
    df_plot["Time"] = np.array(corrected_time).T.flatten()
    df_plot["Amplitude"] = np.array(amplitude_wfms).T.flatten()

    # wfm averaging with 2 decimals and mean combination method
    df_plot = df_plot.sort_values("Time").groupby("Time").mean().reset_index()
    df_plot = df_plot.sort_values("Time").round(1).groupby("Time").mean()

    # plot wfm wfm averaging on top of data points
    spline_param = splrep(x=df_plot.index.values, y=df_plot["Amplitude"], s=2000)
    x_plot_spline = np.arange(df_plot.index.values.min(), df_plot.index.values.max(), 0.01)
    y_plot_spline = splev(x_plot_spline, spline_param)


    return x_plot_spline, y_plot_spline, corrected_time