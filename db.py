# Python
from pathlib import Path
import json

# Database
import sqlite3

# Data analysis
import pandas as pd

# Geo
import geopandas as gpd
from shapely.wkb import loads
import shapely.wkb

# Local
import utils


current_path = Path()
conn = sqlite3.connect(current_path / 'data' / 'caf_accessibility.db')


# def save_dataframe_in_sqlite_db(df: pd.DataFrame, table_name: str, conn: sqlite3.Connection=conn):
#     if 'geometry' not in df.columns:
#         raise ValueError('Dataframe must have a geometry column')
#     df['geometry'] = df.apply(lambda x: shapely.wkb.dumps(x.geometry), axis=1)
#     df.to_sql(table_name, conn, if_exists='replace', index=False)


def get_dataframe_from_sqlite_db(table_name: str, conn: sqlite3.Connection=conn, geo_type: str='polygon'):
    # columns = utils.concat_list()   
    columns = '*'
    df = pd.read_sql(f'SELECT {columns} FROM {table_name}', conn)
    if geo_type == 'polygon':
        geo = get_geo_from_sqlite_db(table_name, conn)
    elif geo_type == 'point':
        geo = get_geo_from_sqlite_db(table_name, conn)
        features = geo['features']
        lat = list()
        lon = list()
        for f in features:
            lat.append(f['geometry']['coordinates'][1])
            lon.append(f['geometry']['coordinates'][0])
        geo = pd.DataFrame(data={'lat': lat, 'lon': lon})
    return df, geo

def get_geo_from_sqlite_db(table_name: str, conn: sqlite3.Connection=conn):
    c = conn.cursor()
    c.execute(f'SELECT geometry FROM Geos WHERE table_ = "{table_name}"')
    result = c.fetchone()[0]
    return json.loads(result)

