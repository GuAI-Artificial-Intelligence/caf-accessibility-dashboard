# Local 
import constants

# Geo
import geopandas as gpd

def concat_list(list=(constants.CATEGORICAL_VARIABLES + constants.NON_CATEGORICAL_VARIABLES)):
    return ", ".join(list)

# function to transform geometry column of geopandas into a dict in the format of json
def transform_geometry_to_dict(df: gpd.GeoDataFrame):
    df['geometry'] = df.apply(lambda x: x.geometry.__geo_interface__, axis=1)
    return df