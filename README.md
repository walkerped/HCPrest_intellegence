# HCPrest_intellegence

learn.ipynb presents machine learning model that predicts intellegence from patterns of brain connectivity, as measured by resting state fMRI.

The steps to run the analysis yourself are:

1. Download the data from https://db.humanconnectome.org/data/projects/HCP_1200. You will need to create a login and accept there data use policy to access the data. You will need the file behavioral_data.csv (by clicking the "Behavioral Data" link, under "Quick Downloads") and the zip folder HCP1200_Parcellation_Timeseries_Netmats.zip (by clicking the "CIFTI Subject-specific Parcellations for 15-, 25-, 50-, 100-dimensionalities" link under "Subject-specific ICA parcellations (node maps)").
2. Run prepData.py. The usage for this script is prepData.py [-h] HCP_zip HCP_beh output_dir where HCP_zip is the path to HCP1200_Parcellation_Timeseries_Netmats.zip, HCP_beh is the path to behavioral_data.csv and output_dir is the path where the data should be unpacked to.
3. Open learn.ipynb in jupyter notebook and set the data_dir variable in the second cell to the path where you unpacked the data. You can also tinker with using the brain connectivity data to predict other outcome variables by changing the y_var variable to a column name in behavioral_data.csv. 