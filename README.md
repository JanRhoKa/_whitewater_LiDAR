# Evaluation of full-waveform bottom return extraction in whitewater rapids using bathymetric LiDAR

Code used in the study "Evaluation of full-waveform bottom return extraction in whitewater rapids using bathymetric LiDAR" (Rhomberg-Kauert et al., 2025a).

## Study Abstract
The application of LiDAR and remote sensing methods has long been considered challenging or unfeasible in the turbulent waters of whitewater rapids. Therefore, this study presents a method to survey whitewater rapids using signal processing of full-waveform LiDAR recordings. The subtraction of an idealized water column backscattering response from the recorded waveform and further analysis of the remaining signal allows the extraction of bottom echoes on a single-waveform basis. To evaluate the extracted points, we surveyed a block ramp with both total station measurements and helicopter-based bathymetric LiDAR. We could demonstrate an increase in the water bottom coverage in whitewater areas through the application of the presented method, which is able to extract bottom echoes for 70% of the waveforms in the surveyed area. This improves LiDAR full-waveform processing, by extracting bottom echoes where current processing algorithms were not able to and thus reducing the mean absolute vertical distance to the reference data from 43.9 cm to 13.3 cm.

## Code setup

To run the notebooks and the provided code of the method, the following folder structure has to be implemented after downloading the files ():

### _whitewater_LiDAR
- data
  - all_new_points.txt
  - all_reference.txt
  - pielach_whitewater.txt
  - pielach.txt
  - waveform_data.df
- method
  - __init__.py
  - bathy_convolution.py
  - clean_data.py
  - metrics_and_plotting.py
  - waveform_plotting.py
  - wfm_averaging.py 
- Pielach_Waverforms.ipynb
- Pielach_Whitewater.ipynb
  

## References
Jan Rhomberg-Kauert, Lucas Dammert, Theresa Himmelsbach, et al. "Evaluation of full-waveform bottom return extraction in whitewater rapids using bathymetric LiDAR", Proc. SPIE 13666, Remote Sensing for Agriculture, Ecosystems, and Hydrology XXVII, 1366612 (30 Oct 2025); https://doi.org/10.1117/12.3068055%20.

Rhomberg-Kauert, J., T. Himmelsbach, F. Pöppl, L. Dammert, M. Pfennigbauer, and G. Mandlburger. 2026. “ Mapping River Bed Topography in Whitewater Rapids Using Bathymetric LiDAR .” River Research and Applications 42, no. 4: 886–900. https://doi.org/10.1002/rra.70109%20.
