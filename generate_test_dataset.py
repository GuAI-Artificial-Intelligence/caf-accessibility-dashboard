# Python
import random

# Data analysis
import pandas as pd
import numpy as np

# Local
from constants import CENTER_CITY_COORDINATES

# # Define the center latitude and longitude for Bogota
# center_lat = 4.7110
# center_lon = -74.0721

def gen_random_points(center_lat, center_lon, city):

    # Generate 1000 random latitude and longitude values around city
    latitude = np.random.normal(center_lat, 0.1, 1000)
    longitude = np.random.normal(center_lon, 0.1, 1000)

    # Generate 1000 random accesibility values
    accessibility_foot = np.random.randint(0, 100, 1000)
    accessibility_bicycle = np.random.randint(0, 100, 1000)
    accessibility_car = np.random.randint(0, 100, 1000)

    # Random neighborhood
    neighborhood =[city + " Barrio " + str(random.randint(1, 50)) for i in range(len(accessibility_foot))]

    # Create a Pandas DataFrame with the data
    df = pd.DataFrame(
        {
            "latitude": latitude, 
            "longitude": longitude,
            "accessibility_foot": accessibility_foot, 
            "accessibility_bicycle": accessibility_bicycle, 
            "accessibility_car": accessibility_car,
            "neighborhood": neighborhood,
        }
    )

    df['city'] = city

    # By neighborhood
    cols = ['city', 'neighborhood', 'accessibility_foot', 'accessibility_bicycle', 'accessibility_car']
    df_neighborhood = df[cols].groupby(['city', 'neighborhood']).mean().reset_index()

    # Generate random population values
    population = np.random.randint(20000, 100000, df_neighborhood.shape[0])
    df_neighborhood['population'] = population
    df_neighborhood['latitude'] = np.random.normal(center_lat, 0.1, df_neighborhood.shape[0])
    df_neighborhood['longitude'] = np.random.normal(center_lon, 0.1, df_neighborhood.shape[0])

    return df, df_neighborhood

if __name__ == '__main__':

    dfs = list()
    df_neighborhoods = list()
    for city in CENTER_CITY_COORDINATES.keys():
        df, df_neighborhood = gen_random_points(
            CENTER_CITY_COORDINATES[city]["center_lat"],
            CENTER_CITY_COORDINATES[city]["center_lon"],
            city
        )
        dfs.append(df)
        df_neighborhoods.append(df_neighborhood)

    pd.concat(dfs).to_csv('data/test_bogota_cuenca_data.csv', index=False)
    pd.concat(df_neighborhoods).to_csv('data/test_bogota_cuenca_neighborhoods_data.csv', index=False)