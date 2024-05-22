# SurfaceWaterExtentTimeSeriesAnalysis

Guide to run the script for representing the surface water area of the inland waterbody and depicting the time series of the surface water extent values is demonstrated step by step:
•	Set up the environment:
o	Installation of required libraries viz.  geopandas, earthengine-api, pandas, and numpy.
o	Use “pip install geopandas pandas earthengine-api matplotlib” in the terminal for installation.
•	Initialize the Google Earth Engine API
o	You need to authenticate with Google Earth Engine (GEE). Follow the instructions on their authentication guide.
o	Use “ee.Authenticate()” in the script  for verification of authentication of GEE.
•	Load the GeoJSON file
o	Utilise geopandas library to load the GeoJSON file.
•	Fetch surface water data from GEE
o	Query out the dataset and calculate the Spectral index MNDWI for water bodies detection. 
•	Process and aggregate the data:
o	Calculate the surface water extent time series for the specified water body.
•	Generate the time series dataframe
o	Use pandas to structure out the output as time series dataframe comprising dates and water area. 
Notes: 
•	In the Script, provide the actual path of input parameters viz. GeoJSON file, the desired date range, and the path to save the plot image.
•	Make sure the GeoJSON file contains a valid polygon representing the inland water body.
•	Sentinel-2 dataset which provides high resolution (10m spatial resolution) images, is used to calculate Modified Normalized difference Water index (MNDWI) for detecting the water bodies. MNDWI utilises Green and Short wave infrared bands which are B3 and B11 respectively in Sentinel-2 dataset. 
•	The threshold of ‘0’ is typically set in MNDWI images for water detection; but can be altered a bit depending upon the actual conditions of the area of interest.
•	The script will output the time series of surface water extent values for the specified period and save the plot as an image file.
