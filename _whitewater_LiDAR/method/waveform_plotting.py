import numpy as np
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from .bathy_convolution import fit_curve_whitewater


def plot_multiple_wfms(wfm_selected, color, panel, sample_intervals):
    """
        Plot the 200 first waveforms of given dataset (wfm_selected) and return amplitudes.
    """
    
    list_amplitudes = []
    for wfm in wfm_selected[:200]:

        # split standard wfm data
        wfm = np.array(wfm).T
        wfm_selected_y = wfm[1]
        wfm_selected_x = wfm[0] - wfm[0][0]

        # get amplitudes up to 25 samples
        list_amplitudes.append(wfm_selected_y[:25])

        # plot wfm over time [ns]
        ax = sns.lineplot(x=wfm_selected_x * sample_intervals * 1e9, y=wfm_selected_y, color=color, alpha=0.1)

    # add plot info
    ax.set_xlabel("Time [ns]")
    ax.set_ylabel("Amplitude [ADC]")
    ax.set_xlim(-1, 25 * sample_intervals * 1e9)
    ax.text(0, 1.05, panel, fontsize=25, transform=ax.transAxes)

    return ax, list_amplitudes


def plot_averaging(df_0_wfms, df_1000_wfms, df_2000_wfms, df_3000_wfms):
    """
        Create waveform averaging of the given wfms. 
    """

    # set basics
    c = 299792458
    n_water = 1.33
    palette = ["#E18922", "#BA4682", "#007E71", "#006699"]

    # create df multi-plot parameter
    data_0 = df_0_wfms.assign(Max_ampl="1000")
    data_1000 = df_1000_wfms.assign(Max_ampl="2000")
    data_2000 = df_2000_wfms.assign(Max_ampl="3000")
    data_3000 = df_3000_wfms.assign(Max_ampl="4000")

    # merge dataframes
    concat_data_single_df = pd.concat([data_0, data_1000, data_2000, data_3000])    
    merge_to_plot_format = pd.melt(concat_data_single_df, id_vars=['Max_ampl'], var_name="Time [ns]")

    # plot individual samples
    ax = sns.stripplot(x="Time [ns]", y="value", hue="Max_ampl", data=merge_to_plot_format, dodge=True, alpha=0.075, palette=palette)       

    # average waveforms
    line_plot_df = concat_data_single_df.groupby(["Max_ampl"]).mean().T

    # adjust line plot to spacing of strip plot
    x_values_plot = line_plot_df.index * 2

    # plot averaged waveforms
    ax = sns.lineplot(x=x_values_plot, y=line_plot_df["1000"].values, color=palette[0], linewidth=3)
    ax = sns.lineplot(x=x_values_plot, y=line_plot_df["2000"].values, color=palette[1], linewidth=3)
    ax = sns.lineplot(x=x_values_plot, y=line_plot_df["3000"].values, color=palette[2], linewidth=3)
    ax = sns.lineplot(x=x_values_plot, y=line_plot_df["4000"].values, color=palette[3], linewidth=3)

    # add legend
    patch_3 = mpatches.Patch(color=palette[0], label='<1000 amplitude')
    patch_2 = mpatches.Patch(color=palette[1], label='<2000 amplitude')
    patch_1 = mpatches.Patch(color=palette[2], label='<3000 amplitude')
    patch_0 = mpatches.Patch(color=palette[3], label='<4000 amplitude')
    plt.legend(handles=[patch_0, patch_1, patch_2, patch_3], fontsize=12, markerscale=0.5, loc='upper right')

    # create second scale for distance in water
    ax2 = ax.twiny()
    ax2.set_xticks(ax.get_xticks())
    ax2.set_xbound(ax.get_xbound())
    ax2.set_xlabel("Distance water [m]")
    ax2.set_xticklabels([np.round(x * c * 1e-9 / n_water, 2)  for x in data_3000.columns[:-1]])

    # add y axis info
    ax.set_ylim(-50, 4250)
    ax.set_ylabel("Amplitude")
    ax.text(0, 1.05, "A", fontsize=25, transform=ax.transAxes)

    return ax


def plot_wfm_fitting(data_columns, line_plot_data, panel, color, max_y):
    """
        Plot fitting of convolution for the given waveform.
    """

    # fit idealized water column to data
    x_optimize, y_optimize, convolution = fit_curve_whitewater(data_columns, line_plot_data)

    # plot recorded waveform data
    ax = sns.lineplot(x=data_columns, y=line_plot_data, color=color, linewidth=4, alpha=0.8)

    # plot fitting and residual
    ax = sns.lineplot(x=x_optimize, y=convolution, color="black")
    ax = sns.lineplot(x=x_optimize, y=y_optimize - convolution, color="black", linestyle="--", linewidth=1.7)

    # add plot info
    ax.set_ylim((0, max_y))
    ax.set_xlabel("Time [ns]")
    ax.set_ylabel("Amplitude [ADC]")
    ax.text(0, 1.05, panel, fontsize=25, transform=ax.transAxes)

    return ax
