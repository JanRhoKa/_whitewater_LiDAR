import numpy as np
from sklearn.cluster import DBSCAN


def clean_lidar_df(las_df, epsilon=0.3, outlier_or_max_cluster="max_cluster"):
    """
        Remove outliers with clustering.
    """

    # cluster the data with standard parameter to remove outliers
    coordinates = las_df[["x", "y", "z"]]
    labels = DBSCAN(epsilon).fit_predict(coordinates)

    #
    if outlier_or_max_cluster == "max_cluster":
        # 
        values, counts = np.unique(labels, return_counts=True)
        max_label = values[np.argmax(counts)]

        # create new df without noise
        las_df_cleaned = las_df[labels == max_label]

    else:
        # create new df without noise
        las_df_cleaned = las_df[labels != -1]
        

    return las_df_cleaned