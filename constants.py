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