# Python
import json 
from pathlib import Path
import time
from urllib.request import urlopen

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


# bogota_h3_gdf = gpd.read_file(
#     current_path / 'data' / 'Bogota_new_shape_h3_child.geojson'
#     )


bogota_cuenca_gdf = gpd.read_file(
    current_path / 'data' / 'bogota_cuenca_v1.geojson'
)

bogota_gdf = bogota_cuenca_gdf[bogota_cuenca_gdf.city=='Bogotá'].copy()
cuenca_gdf = bogota_cuenca_gdf[bogota_cuenca_gdf.city=='Cuenca'].copy()

del bogota_cuenca_gdf

# --
locations = bogota_gdf.index.values
variable = 'NSE_5'
geojson_bogota = bogota_gdf.geometry
geojson_cuenca = cuenca_gdf.geometry


def get_hex_map(city, variable='NSE_5'):

    lat = constants.CENTER_CITY_COORDINATES[city]['center_lat']
    lon = constants.CENTER_CITY_COORDINATES[city]['center_lon']

    categorical_variable = False
    if variable in ['NSE_3', 'NSE_5']:
        categorical_variable = True

    if city=='Bogotá':
        zoom = 10
        data = bogota_gdf
        geojson = geojson_bogota

    if city=='Cuenca':
        zoom = 11.5
        data = cuenca_gdf
        geojson = geojson_cuenca

    if categorical_variable:
        if variable=='NSE_3':
            color_discrete_map = {
                '1 - Alto':'#daa98a',
                '2 - Medio':'#b63c3f',
                '3 - Bajo':'#311a3c'
            }
            category_orders={
                'NSE_3' : [
                    '1 - Alto',
                    '2 - Medio',
                    '3 - Bajo'
                ]
            }

        if variable=='NSE_5':
            color_discrete_map = {
                '1 - Alto':'#daa98a',
                '2 - Medio-Alto':'#ae6045',
                '3 - Medio':'#b63c3f',
                '4 - Medio-Bajo':'#922651',
                '5 - Bajo':'#311a3c'
            }
            category_orders={
                'NSE_5' : [
                    '1 - Alto',
                    '2 - Medio-Alto',
                    '3 - Medio',
                    '4 - Medio-Bajo',
                    '5 - Bajo'
                ]
            }

        fig_hex_map = px.choropleth_mapbox(
            data_frame=data[variable], 
            geojson=geojson, 
            locations=data.index,
            color=variable,
            color_continuous_scale="Turbo",
            mapbox_style="carto-positron",
            zoom=zoom, 
            center = {"lat": lat, "lon": lon},
            opacity=0.4,
            color_discrete_map=color_discrete_map,
            category_orders=category_orders
        )
        fig_hex_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig_hex_map.update_layout(
            showlegend=True,
            legend=dict(
                x=0.95,
                y=0.05,
                xanchor='right',
                yanchor='bottom'
            ),

        )
    else:
        max_range = max(data[variable])
        fig_hex_map = px.choropleth_mapbox(
            data_frame=data[variable], 
            geojson=geojson, 
            locations=data.index,
            color=variable,
            range_color=(1, max_range),
            color_continuous_scale="Turbo",
            mapbox_style="carto-positron",
            zoom=zoom, 
            center = {"lat": lat, "lon": lon},
            opacity=0.4,
            )
        fig_hex_map.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
        )
        fig_hex_map.update_coloraxes(colorbar_orientation='v')
        fig_hex_map.update_coloraxes(colorbar_thickness=10)
        # fig_hex_map.update_coloraxes(colorbar_title=dict(text=''))
        fig_hex_map.update_coloraxes(colorbar_y=0.15)
        fig_hex_map.update_coloraxes(colorbar_x=0.88)
        fig_hex_map.update_coloraxes(colorbar_len=0.2)
        fig_hex_map.update_coloraxes(colorbar_tickfont=dict(color="#323232"))

    return fig_hex_map


# def get_selector_graph(city, accesibility_means):

#     fig = px.scatter(
#         dataset_neighborhoods[dataset_neighborhoods.city == city],
#         x=constants.ACCESIBILITY_MEANS[accesibility_means],
#         y="population",
#         size="population",
#         color=constants.ACCESIBILITY_MEANS[accesibility_means],
#         hover_name="neighborhood",
#         log_x=False,
#         size_max=20,
#         height=250,
#     )

#     fig.update_yaxes(visible=False, showticklabels=False)
#     fig.update_xaxes(visible=False, showticklabels=False)
#     fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
#     fig.update_layout(showlegend=False)
#     fig.update_layout(plot_bgcolor="#343332")
#     fig.update_traces(marker_sizemin=3, selector=dict(type='scatter'))

#     fig.update_coloraxes(colorbar_orientation='h')
#     fig.update_coloraxes(colorbar_thickness=10)
#     fig.update_coloraxes(colorbar_title=dict(text=''))
#     fig.update_coloraxes(colorbar_y=0.0)
#     fig.update_coloraxes(colorbar_x=0.5)
#     fig.update_coloraxes(colorbar_len=0.3)
#     fig.update_coloraxes(colorbar_tickfont=dict(color="#f4f4f4"))

#     return fig


# def get_centered_map(city, accesibility_means, neighborhood):
    
#     if neighborhood is None:
#         lat = constants.CENTER_CITY_COORDINATES[city]['center_lat']
#         lon = constants.CENTER_CITY_COORDINATES[city]['center_lon']
#         zoom = 10
#     else:
#         lat = dataset_neighborhoods[dataset_neighborhoods.neighborhood==neighborhood].latitude.values[0]
#         lon = dataset_neighborhoods[dataset_neighborhoods.neighborhood==neighborhood].longitude.values[0]
#         zoom = 12

#     fig = px.density_mapbox(
#         dataset,
#         lat="latitude",
#         lon="longitude",
#         z=constants.ACCESIBILITY_MEANS[accesibility_means],
#         radius=10,
#         hover_name="city",
#         hover_data=["city", "accessibility_foot"],
#         center=dict(lat=lat, lon=lon),
#         zoom=zoom,
#         opacity=1,
#         mapbox_style="carto-darkmatter",
#         # mapbox_style="open-street-map",

#     )
#     fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
#     fig.update_coloraxes(colorbar_orientation='v')
#     fig.update_coloraxes(colorbar_thickness=10)
#     fig.update_coloraxes(colorbar_title=dict(text=''))
#     fig.update_coloraxes(colorbar_y=0.2)
#     fig.update_coloraxes(colorbar_x=0.92)
#     fig.update_coloraxes(colorbar_len=0.3)
#     fig.update_coloraxes(colorbar_tickfont=dict(color="#f4f4f4"))
#     token = MAPBOX_TOKEN
#     fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
#     return fig


# fig = get_centered_map(
#     list(constants.CENTER_CITY_COORDINATES.keys())[0], 
#     list(constants.ACCESIBILITY_MEANS.keys())[0],
#     None
#     )


fig_hex_map = get_hex_map(
    list(constants.CENTER_CITY_COORDINATES.keys())[0]
)

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
                                options=['NSE_3', 'NSE_5', 'Poblacion'],
                                value='NSE_5',
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



@ app.callback(
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
    return get_hex_map(city, variable)
    



# @ app.callback(
#     [
#         Output(component_id=constants.MAP_ID, component_property='figure'),
#         # Output(component_id=constants.SCATTER_ID, component_property='figure')
#     ],
#     [
#         Input(component_id=constants.CITY_SELECTOR, component_property='value'),
#         Input(component_id=constants.ACCESIBILITY_SELECTOR,
#               component_property='value'),
#         # Input(component_id=constants.SCATTER_ID,
#         #       component_property='hoverData'),
#     ]
# )
# def update_output_div(city, accesibility_means):
# # def update_output_div(city, accesibility_means, clicked_neighborhoods):
#     triggered_input = ctx.triggered_id
#     # if ((triggered_input == constants.SCATTER_ID or triggered_input == constants.ACCESIBILITY_SELECTOR) and (clicked_neighborhoods!= None)):
#     #     neighborhood =  clicked_neighborhoods['points'][0]['hovertext']
#     # else:
#     #     neighborhood = None
#     return get_hex_map(city)
#     #return get_centered_map(city, accesibility_means, neighborhood), get_selector_graph(city, accesibility_means)


# Run the app
if __name__ == '__main__':
    app.run_server(
        debug=True,
        host='0.0.0.0', 
        port=8050
        )

