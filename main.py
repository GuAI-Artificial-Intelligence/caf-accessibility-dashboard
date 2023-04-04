# Python
import json 
from pathlib import Path
import time
import sys


# Data Analysis
import pandas as pd
import geopandas as gpd
import numpy as np

# Plotly
import plotly.express as px
import plotly.graph_objects as go

# Dash
from dash import Dash, dcc, html, Input, Output, ctx

# Bootstrap
import dash_bootstrap_components as dbc

# Local
import constants

# Credentials
from conf.credentials import MAPBOX_TOKEN

current_path = Path()



bogota_cuenca_df_csv = pd.read_csv(current_path / 'data' / 'bogota_cuenca_v1.csv')
bogota_cuenca_gdf_geo = gpd.read_file(
    current_path / 'data' / 'bogota_cuenca_geo_v1.geojson',
)


geojson_bogota_cuenca = bogota_cuenca_gdf_geo.geometry



def init_map(df=bogota_cuenca_df_csv, geodf=geojson_bogota_cuenca, variable='NSE_5', city=constants.BOGOTA_STR):
    z = df[variable].map(constants.NSE_5_DICTMAP).values
    colorbar = constants.CATEGORICAL_COLORBAR
    colorbar['tickvals'] = constants.NS5_TICKVALS
    colorbar['ticktext'] = constants.NS5_TICKTEXT
    colorbar['title'] = '<b>Nivel socio<br>económico</b><br> .'
    fig_hex_map = go.Figure(
        go.Choroplethmapbox(
            geojson=json.loads(geodf.to_json()), 
            z=z,
            locations=pd.Series(df.index.values).astype(str), 
            colorbar=colorbar,
            colorscale=constants.NS5_COLORSCALE,
            marker_opacity=0.4
        )
    )

    fig_hex_map.update_layout(
        mapbox_accesstoken=MAPBOX_TOKEN,
        mapbox_center = {
            "lat": constants.CENTER_CITY_COORDINATES[city]['center_lat'], 
            "lon": constants.CENTER_CITY_COORDINATES[city]['center_lon']
        },
        mapbox_zoom=10,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    return fig_hex_map
    

fig_hex_map = init_map()


# end_time2 = time.time()

# elapsed_time = end_time - start_time
# elapsed_time2 = end_time2 - start_time2
# print(f"Elapsed time (2): {elapsed_time} seconds")
# print(f"Elapsed time (3): {elapsed_time2} seconds")



def update_hex_map(city, fig_hex_map, variable=constants.CATEGORICAL_VARIABLES[1], df=bogota_cuenca_df_csv):


    lat = constants.CENTER_CITY_COORDINATES[city]['center_lat']
    lon = constants.CENTER_CITY_COORDINATES[city]['center_lon']

    nse_variable = False
    if variable in constants.CATEGORICAL_VARIABLES:
        nse_variable = True

    if city==constants.BOGOTA_STR:
        zoom = 10

    if city==constants.CUENCA_STR:
        zoom = 11.5

    if nse_variable:
        colorbar = constants.CATEGORICAL_COLORBAR
        if variable==constants.CATEGORICAL_VARIABLES[0]:
            z = df[variable].map(constants.NSE_3_DICTMAP).values
            colorbar['tickvals'] = constants.NS3_TICKVALS
            colorbar['ticktext'] = constants.NS3_TICKTEXT
            zmax=3
        if variable==constants.CATEGORICAL_VARIABLES[1]:
            z = df[variable].map(constants.NSE_5_DICTMAP).values
            colorbar['tickvals'] = constants.NS5_TICKVALS
            colorbar['ticktext'] = constants.NS5_TICKTEXT
            zmax=5
        colorbar['title'] = '<b>Nivel socio<br>económico</b><br> .'
        # fig_hex_map.update_traces(
        #     overwrite=True,
        #     z=z,
        #     zmin=0,
        #     zmax=zmax,
        #     colorscale='Magma',
        #     colorbar=colorbar,
        #     selector=dict(type='choroplethmapbox'),
        # )
    else:
        z = df[variable]
        indices = np.where(df['city'] == city)
        zmax = df[variable].values[indices].max()
        colorbar = constants.CATEGORICAL_COLORBAR
        colorbar['title'] = f'<b>{variable}</b><br> .'
        colorbar['tickmode'] = 'auto'

    fig_hex_map.update_traces(
        overwrite=True,
        z=z,
        zmin=0,
        zmax=zmax,
        colorscale='Magma',
        colorbar=colorbar,
        selector=dict(type='choroplethmapbox'),
    )
    fig_hex_map.update_layout(
        mapbox_center = {
            "lat": lat, 
            "lon": lon
        },
        mapbox_zoom=zoom, 
    )



    return fig_hex_map




# Create a Dash app
app = Dash(
    external_stylesheets=['assets/base.css', dbc.themes.BOOTSTRAP]
)

app.layout = html.Div(
    [dbc.Row(
        children=[
            dbc.Col(
                width=4,
                className='panel-control-container',
                children=[
                    html.Div(
                        children=[
                            html.H5("Accesibilidad en Bogotá y Cuenca",
                                    className="card-title"),
                            html.P(
                        "       Esta plataforma busca responder"
                                " ¿cómo es la accesibilidad en Bogotá según el tipo de usuario?"
                                " En la sección de abajo encontrará menus para que juegue y vea"
                                "qué tan accesibles son las oportunidades para personas"
                                "según su modo de transporte",
                                className="card-text",
                            ),
                            html.H6('Ciudad'),
                            dcc.Dropdown(
                                options=list(constants.CENTER_CITY_COORDINATES.keys()),
                                value=list(constants.CENTER_CITY_COORDINATES.keys())[0],
                                id=constants.CITY_SELECTOR,
                                clearable=False
                            ),
                            html.H6('Variable'),
                            dcc.Dropdown(
                                options=constants.CATEGORICAL_VARIABLES+constants.NON_CATEGORICAL_VARIABLES,
                                value=constants.CATEGORICAL_VARIABLES[1],
                                id='my-variable-selector',
                                clearable=False
                            ),
                            # html.H6('Medio de acceso'),
                            # dcc.Dropdown(
                            #     options=list(constants.ACCESIBILITY_MEANS.keys()),
                            #     value=list(constants.ACCESIBILITY_MEANS.keys())[0],
                            #     id=constants.ACCESIBILITY_SELECTOR,
                            #     clearable=False
                            # ),
                        ],
                        className='panel-control-content'
                    ),
                ]
            ),
            dbc.Col(
                width=8,
                children=[
                    dbc.Row(
                        children=[
                            html.Div(
                                children=[
                                    dcc.Graph(
                                        figure=fig_hex_map,
                                        style={"height": "100%",
                                               "width": "100%"},
                                        config={
                                            'displayModeBar': False
                                        },
                                        id=constants.MAP_ID
                                    )
                                ],
                                className='map-content'
                            ),
                        ],
                    ),
                    # dbc.Row(
                    #     [html.P("Seleccione un punto de la gráfica para ver los datos de una localidad.", className='graph-selector-text'),
                    #      dcc.Graph(
                    #         id=constants.SCATTER_ID,
                    #         figure=get_selector_graph(
                    #             list(constants.CENTER_CITY_COORDINATES.keys())[0],
                    #             list(constants.ACCESIBILITY_MEANS.keys())[0]
                    #         ),
                    #         config={
                    #             'displayModeBar': False
                    #         },
                    #         style={"height": "100%",
                    #                "width": "100%"},
                    #     )],
                    # ),
                ],
                className='map-container'
            ),
        ]
    ),
    ]
)



@app.callback(
        Output(component_id=constants.MAP_ID, component_property='figure'),
    
        [
        Input(component_id=constants.CITY_SELECTOR, component_property='value'),
        Input(component_id='my-variable-selector', component_property='value')
        
    ],
        # Input(component_id=constants.ACCESIBILITY_SELECTOR,
        #       component_property='value'),
        # Input(component_id=constants.SCATTER_ID,
        #       component_property='hoverData'),
    
)
def update_output_div(city, variable):
    triggered_input = ctx.triggered_id
    return update_hex_map(city=city, fig_hex_map=fig_hex_map, variable=variable)
    






# Run the app
if __name__ == '__main__':
    app.run_server(
        debug=True,
        host='0.0.0.0', 
        port=8050
        )

