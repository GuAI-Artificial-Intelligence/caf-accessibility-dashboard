import geopandas as gpd
import pandas as pd


bogota = gpd.read_file(
    'Bogota_new_shape_h3_child.geojson'
)

cuenca = gpd.read_file(
    'cuenca_hexs10.geojson'
)   


cuenca.rename(
    columns={
        'Pob_tot': 'Poblacion',
        'PCA_1': 'PCA'
    },
    inplace=True
)
cuenca['city'] = 'Cuenca'

bogota.rename(
    columns={
        'NSE3': 'NSE_3',
        'NSE': 'NSE_5'
    },
    inplace=True
)
bogota['city'] = 'Bogotá'

ns3_map = {
    '3 Bajo':'3 - Bajo',     
    '1 Alto': '1 - Alto',     
    '2 Medio': '2 - Medio'    
}
bogota.NSE_3 = bogota.NSE_3.map(ns3_map)


ns5_map = {
    '5 Bajo':'5 - Bajo',          
    '1 Alto':'1 - Alto',          
    '2 Medio-Alto':'2 - Medio-Alto',     
    '4 Medio-Bajo':'4 - Medio-Bajo',     
    '3 Medio':'3 - Medio'   
}

bogota.NSE_5 = bogota.NSE_5.map(ns3_map)
mix = pd.concat([bogota, cuenca])

mix.to_file('bogota_cuenca_v1.geojson', driver='GeoJSON')