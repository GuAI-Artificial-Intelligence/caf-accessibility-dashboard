import pandas as pd
import numpy as np

from constants import CENTER_CITY_COORDINATES

# Define the center latitude and longitude for Bogota
center_lat = 4.7110
center_lon = -74.0721

def gen_random_points(center_lat, center_lon, city):
    # Generate 1000 random latitude and longitude values around Bogota
    latitude = np.random.normal(center_lat, 0.1, 1000)
    longitude = np.random.normal(center_lon, 0.1, 1000)

    # Generate 1000 random population values
    accessibility = np.random.randint(0, 100, 1000)

    # Create a Pandas DataFrame with the data
    df = pd.DataFrame(
        {"Accesibilidad": accessibility, "latitude": latitude, "longitude": longitude})
    df['city'] = city
    
    return df


if __name__ == '__main__':
    # cities = {
    #     'Bogota': {
    #         'center_lat': 4.7110,
    #         'center_lon': -74.0721
    #     },
    #     'Cuenca': {
    #         'center_lat': -2.897213,
    #         'center_lon': -79.003138
    #     }
    # }
    dfs = []
    for city in CENTER_CITY_COORDINATES.keys():
        
        tempdf = gen_random_points(
            CENTER_CITY_COORDINATES[city]["center_lat"], 
            CENTER_CITY_COORDINATES[city]["center_lon"],
            city
        )
        dfs.append(tempdf)
    pd.concat(dfs).to_csv('data/test_bogota_cuenca_data.csv', index=False)