import geopandas as gpd
import ee
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

###Initialize the Earth Engine API###
ee.Authenticate()
ee.Initialize()


###Load the GeoJSON file using GeoPandas###
def load_geojson(filepath):
   
    return gpd.read_file(filepath)

###Get the surface water extent time series for the specified geometry and time range###
def get_surface_water_extent(geometry, start_date, end_date):
  
    # Define the dataset ( Leveraged "JRC Global Surface Water Mapping Layers v1.4" dataset)
    dataset = ee.ImageCollection('JRC/GSW1_4/MonthlyHistory') \
                .filterDate(start_date, end_date) \
                .select('water')
    
    # Function to compute the water area for each image
    def compute_water_area(image):
        water = image.eq(2)  # Water class in the dataset
        water_area = water.multiply(ee.Image.pixelArea()).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=geometry,
            scale=30,
            maxPixels=1e9
        )
        return ee.Feature(None, {
            'date': image.date().format('YYYY-MM-dd'),
            'water_area': water_area.get('water')
        })
    
    # Apply the function over the image collection
    water_areas = dataset.map(compute_water_area)
    
    # Convert the result to a list of dictionaries
    water_areas_list = water_areas.getInfo()['features']
    return [{'date': f['properties']['date'], 'water_area': f['properties']['water_area']} for f in water_areas_list]


###Main function to get the surface water extent time series###
def surface_water_extent_timeseries(geojson_path, start_date, end_date):
  
    gdf = load_geojson(geojson_path)
    geometry = ee.Geometry.Polygon(gdf.geometry[0].__geo_interface__['coordinates'])
    
    water_extent = get_surface_water_extent(geometry, start_date, end_date)
    
    return pd.DataFrame(water_extent)

def plot_time_series(df, output_path):
    """
    Plot the surface water extent time series and save the plot as an image file.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(pd.to_datetime(df['date']), df['water_area'], marker='o', linestyle='-', color='b')
    plt.title('Surface Water Extent Time Series')
    plt.xlabel('Date')
    plt.ylabel('Surface Water Area (sq meters)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.show()
    plt.close()


###Input parameters###
geojson_path = r"Input path of  GeoJSON.geojson file from local environment"
start_date = 'Input the start date'
end_date = 'Input the end date'
output_image_path = r"Provide path in the local environment to save the time series plot"

###Get the surface water extent time series###
time_series_df = surface_water_extent_timeseries(geojson_path, start_date, end_date)

###Plot and save the time series###
plot_time_series(time_series_df, output_image_path)

###Display the DataFrame###
print(time_series_df)
