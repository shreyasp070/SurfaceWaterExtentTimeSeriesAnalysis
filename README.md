# SurfaceWaterExtentTimeSeriesAnalysis

<pre>
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
   o	Query out the dataset and calculate the water extent and compute the water area.
    
•	Process and aggregate the data:
   o	Calculate the surface water extent time series for the specified water body.
    
•	Generate the time series dataframe
   o	Use pandas to structure out the output as time series dataframe comprising dates and water area. 
   
Notes: 
•	In the Script, provide the actual path of input parameters viz. GeoJSON file, the desired date range, and the path to save the plot image.
•	Make sure the GeoJSON file contains a valid polygon representing the inland water body.
•	JRC Monthly Water History, v1.4 dataset comprises temporal distribution of surface water from 1984 to 2021 and provides statistics on the extent and change of those water surfaces. 
•	The data is generated using 4,716,475 scenes from Landsat 5, 7, and 8 acquired between years 1984 and 2021. Each pixel is individually classified into water / non-water using an expert system and the results are collated into a monthly history for the entire time period.
•	In computation of the water area class 2 is selected which signifies the water in the imagery.
•	The script will output the time series of surface water extent values for the specified period and save the plot as an image file.

</pre>
