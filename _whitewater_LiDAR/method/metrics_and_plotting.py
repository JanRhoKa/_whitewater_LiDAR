import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def calculate_distance_reference_point_cloud(reference, coordinates_lidar):
    """
        Get absolute vertical distance to nearest neighbor.
    """

    # get nearest neighbors
    closest_points_lidar_index = [np.argmin(np.linalg.norm(coordinates_lidar - point_reference, axis=1)) for point_reference in reference]
    closest_points_lidar_distance = [np.min(np.linalg.norm(coordinates_lidar - point_reference, axis=1)) for point_reference in reference]

    # filter points by distance and get index of nearest neighbor
    closest_points_lidar_index = [index_lidar if closest_points_lidar_distance[index_ref] < 2 else -1 for index_ref, index_lidar in enumerate(closest_points_lidar_index)]

    # calculate absolute distance
    distances = [np.abs(coordinates_lidar.T[2][index_lidar] - reference.T[2][index_ref]) if index_lidar != -1 else np.nan for index_ref, index_lidar in enumerate(closest_points_lidar_index) ]

    return distances


def calculate_rel_distance_reference_point_cloud(reference, coordinates_lidar):
    """
        Get relative vertical distance to nearest neighbor.
    """

    # get nearest neighbors
    closest_points_lidar_index = [np.argmin(np.linalg.norm(coordinates_lidar - point_reference, axis=1)) for point_reference in reference]
    closest_points_lidar_distance = [np.min(np.linalg.norm(coordinates_lidar - point_reference, axis=1)) for point_reference in reference]

    # filter points by distance and get index of nearest neighbor
    closest_points_lidar_index = [index_lidar if closest_points_lidar_distance[index_ref] < 2 else -1 for index_ref, index_lidar in enumerate(closest_points_lidar_index)]

    # calculate relative distance
    distances = [coordinates_lidar.T[2][index_lidar] - reference.T[2][index_ref] for index_ref, index_lidar in enumerate(closest_points_lidar_index) if index_lidar != -1]

    return distances


def plot_evaluation(distances_before, distances_after, x_limit, x_label, panel):
    """
        Plot distance to reference as a histogram.
    """
    
    # plot histograms
    ax = sns.histplot(distances_after, bins=10, color="#E18922")
    ax = sns.histplot(distances_before, bins=25, color="#006699", alpha=0.65)

    # add plot info
    ax.set_xlim(x_limit)
    ax.set_xlabel(x_label)
    ax.set_title("Pielach")

    # add legend
    patch_0 = mpatches.Patch(color="#006699", label='Before', alpha=0.65)
    patch_1 = mpatches.Patch(color="#E18922", label='After')
    plt.legend(handles=[patch_0, patch_1], fontsize=11, markerscale=0.5, loc='upper right')

    # add figure label
    ax.text(0, 1.05, panel, fontsize=25, transform=ax.transAxes)