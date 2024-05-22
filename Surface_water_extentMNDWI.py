import geopandas as gpd
import pandas as pd
import ee
import json
import matplotlib.pyplot as plt

# Initialize the Earth Engine API
ee.Authenticate()
ee.Initialize()

# Function to extract surface water extent time series using Sentinel-2 and MNDWI
def get_surface_water_extent(geojson_path, start_date, end_date):
    # Load the GeoJSON file
    with open(geojson_path) as f:
        geojson = json.load(f)
    
    # Extract the geometry from the GeoJSON file
    geom = ee.Geometry.Polygon(geojson['features'][0]['geometry']['coordinates'])
    
    # Define the start and end dates
    start_date = ee.Date(start_date)
    end_date = ee.Date(end_date)
    
    # Load the Sentinel-2 Surface Reflectance dataset
    dataset = ee.ImageCollection('COPERNICUS/S2_SR') \
              .filterDate(start_date, end_date) \
              .filterBounds(geom) \
              .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))  # Filter cloudy images

    # Function to calculate MNDWI and water area for each image
    def calculate_water_area(image):
        green = image.select('B3')
        swir = image.select('B11')
        mndwi = green.subtract(swir).divide(green.add(swir)).rename('MNDWI')
        water = mndwi.gt(0)  # MNDWI threshold for water detection
        water_area = water.multiply(ee.Image.pixelArea()).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=geom,
            scale=10,
            maxPixels=1e9
        )
        return image.set('date', image.date().format('YYYY-MM-dd')).set('water_area', water_area.get('MNDWI'))
    
    # Map the function over the filtered dataset
    water_area_images = dataset.map(calculate_water_area)

    # Convert the results to a pandas DataFrame
    def get_water_area_list(image):
        return ee.Feature(None, {
            'date': image.get('date'),
            'water_area': image.get('water_area')
        })
    
    water_area_features = water_area_images.map(get_water_area_list).getInfo()['features']
    
    dates = [feature['properties']['date'] for feature in water_area_features]
    areas = [feature['properties']['water_area'] for feature in water_area_features]
    
    time_series_df = pd.DataFrame({'date': dates, 'water_area': areas})
    
    # Convert the date column to datetime
    time_series_df['date'] = pd.to_datetime(time_series_df['date'])
    
    return time_series_df

# Function to plot and save the time series
def plot_time_series(time_series_df, output_path):
    plt.figure(figsize=(10, 6))
    plt.plot(time_series_df['date'], time_series_df['water_area'], marker='o', linestyle='-')
    plt.title('Surface Water Extent Time Series')
    plt.xlabel('Date')
    plt.ylabel('Water Area (square meters)')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.show()

# Example usage
geojson_path = "Enter the path of GeoJSON.geojson file"
start_date = 'Enter the start date'
end_date = 'Enter the end date'
output_image_path = "Enter the path to save the plot"
# Get the surface water extent time series
water_extent_time_series = get_surface_water_extent(geojson_path, start_date, end_date)

# Plot and save the time series
plot_time_series(water_extent_time_series, output_image_path)