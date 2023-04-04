BOGOTA_STR = 'Bogotá'
CUENCA_STR = 'Cuenca'

CENTER_CITY_COORDINATES = {
    BOGOTA_STR: {
        'center_lat': 4.7110,
        'center_lon': -74.0721
    },
    CUENCA_STR: {
        'center_lat': -2.891889142459372,
        'center_lon': -78.9889487554136
    }
}
ACCESIBILITY_MEANS = {
    "A pie": "accessibility_foot",
    "Bicicleta": "accessibility_bicycle",
    "Carro": "accessibility_car",
}

# Components IDs
SCATTER_ID = "my-scatter"
MAP_ID = 'my-map'
CITY_SELECTOR = 'my-city-selector'
ACCESIBILITY_SELECTOR='my-accesibility-selector'

CATEGORICAL_VARIABLES = ['NSE_3', 'NSE_5']
NON_CATEGORICAL_VARIABLES = ['Poblacion']

NSE_3_DICTMAP = {
    '1 - Alto': 3,      
    '2 - Medio': 2, 
    '3 - Bajo': 1    
}

NSE_5_DICTMAP = {
    '1 - Alto': 5,          
    '2 - Medio-Alto': 4,     
    '3 - Medio': 3,   
    '4 - Medio-Bajo': 2,     
    '5 - Bajo': 1         
}

NS3_COLORSCALE = ['#311a3c', '#b63c3f', '#daa98a']
NS3_TICKVALS = [1, 2, 3]
NS3_TICKTEXT=['Bajo',  'Medio', 'Alto']

NS5_COLORSCALE = ['#311a3c', '#922651', '#b63c3f', '#ae6045', '#daa98a']
NS5_TICKVALS = [1, 2, 3, 4, 5]
NS5_TICKTEXT=['Bajo', 'Medio-Bajo', 'Medio','Medio-Alto', 'Alto']

CATEGORICAL_COLORBAR=dict(
    orientation='v',
    thickness=10,
    y=0.2,
    x=0.88,
    len=0.25,
    tickfont=dict(color="#323232"),
)