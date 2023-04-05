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
import dash
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



def init_map(df=bogota_cuenca_df_csv, geodf=geojson_bogota_cuenca, variable='IndiAcce', city=constants.BOGOTA_STR):
    z = df[variable].map(constants.INDIACCE_DICTMAP).values
    # z = df[variable]
    colorbar = constants.CATEGORICAL_COLORBAR
    colorbar['tickvals'] = constants.INDIACCE_TICKVALS
    colorbar['ticktext'] = constants.INDIACCE_TICKTEXT
    colorbar['title'] = '<b>Accesibilidad</b><br> .'
    fig_hex_map = go.Figure(
        go.Choroplethmapbox(
            geojson=json.loads(geodf.to_json()), 
            z=z,
            locations=pd.Series(df.index.values).astype(str), 
            colorbar=colorbar,
            colorscale='Magma',
            marker_opacity=1
        )
    )

    fig_hex_map.update_layout(
        mapbox_accesstoken=MAPBOX_TOKEN,
        mapbox_center = {
            "lat": constants.CENTER_CITY_COORDINATES[city]['center_lat'], 
            "lon": constants.CENTER_CITY_COORDINATES[city]['center_lon']
        },
        mapbox_zoom=9.5,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    return fig_hex_map
    

fig_hex_map = init_map()


# end_time2 = time.time()

# elapsed_time = end_time - start_time
# elapsed_time2 = end_time2 - start_time2
# print(f"Elapsed time (2): {elapsed_time} seconds")
# print(f"Elapsed time (3): {elapsed_time2} seconds")



def update_hex_map(city, fig_hex_map, variable='IndiAcce', df=bogota_cuenca_df_csv):


    lat = constants.CENTER_CITY_COORDINATES[city]['center_lat']
    lon = constants.CENTER_CITY_COORDINATES[city]['center_lon']

    nse_variable = False
    if variable in constants.CATEGORICAL_VARIABLES:
        nse_variable = True

    if city==constants.BOGOTA_STR:
        zoom = 9.5

    if city==constants.CUENCA_STR:
        zoom = 11.5

    if nse_variable:
        colorbar = constants.CATEGORICAL_COLORBAR
        if variable==constants.CATEGORICAL_VARIABLES[0]:
            z = df[variable].map(constants.INDIACCE_DICTMAP).values
            colorbar['tickvals'] = constants.INDIACCE_TICKVALS
            colorbar['ticktext'] = constants.INDIACCE_TICKTEXT
            zmax=4
            colorbar['title'] = '<b>Accesibilidad</b><br> .'
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


def get_bar_figure():

    nse = bogota_cuenca_df_csv.NSE_5.unique()
    nse = [    
        '1 - Alto',          
        '2 - Medio-Alto',     
        '3 - Medio',   
        '4 - Medio-Bajo',     
        '5 - Bajo' 
    ]
    y1 = bogota_cuenca_df_csv[bogota_cuenca_df_csv.IndiAcce=='1. Alta'][['NSE_5', 'Poblacion']].groupby('NSE_5').sum()['Poblacion'].values
    y2 = bogota_cuenca_df_csv[bogota_cuenca_df_csv.IndiAcce=='2. Media Alta'][['NSE_5', 'Poblacion']].groupby('NSE_5').sum()['Poblacion'].values
    y3 = bogota_cuenca_df_csv[bogota_cuenca_df_csv.IndiAcce=='3. Media Baja'][['NSE_5', 'Poblacion']].groupby('NSE_5').sum()['Poblacion'].values
    y4 = bogota_cuenca_df_csv[bogota_cuenca_df_csv.IndiAcce=='4. Baja'][['NSE_5', 'Poblacion']].groupby('NSE_5').sum()['Poblacion'].values
    
    

    animals=['giraffes', 'orangutans', 'monkeys']

    fig = go.Figure(data=[
        go.Bar(name='Baja', x=nse, y=y4, width=0.4, marker_color='#491874'),
        go.Bar(name='Media-Baja', x=nse, y=y3, width=0.4, marker_color='#a84276' ),
        go.Bar(name='Media-Alta', x=nse, y=y2, width=0.4, marker_color='#eb8f6d'),
        go.Bar(name='Alta', x=nse, y=y1, width=0.4, marker_color='#fcfdc6'),
        # go.Bar(name='SF Zoo', x=animals, y=[20, 14, 23]),
        # go.Bar(name='LA Zoo', x=animals, y=[12, 18, 29])
    ])
    # Change the bar mode
    

    # fig.update_yaxes(visible=False, showticklabels=False)
    # fig.update_xaxes(visible=False, showticklabels=False)
    
    fig.update_layout(
        xaxis_title="Nivel socioeconómico",
        yaxis_title="Habitantes",
        legend_title="Accesibilidad",
        margin=dict(l=0, r=0, t=20, b=20),
        barmode='stack',
        # plot_bgcolor='white',
        paper_bgcolor='#323232',
        plot_bgcolor="#323232",
        font=dict(
            color="white"
        ),

    )
    
    # fig.update_layout(showlegend=False)

    # fig.update_traces(marker_sizemin=3, selector=dict(type='scatter'))

    # fig.update_coloraxes(colorbar_orientation='h')
    # fig.update_coloraxes(colorbar_thickness=10)
    # fig.update_coloraxes(colorbar_title=dict(text=''))
    # fig.update_coloraxes(colorbar_y=0.0)
    # fig.update_coloraxes(colorbar_x=0.5)
    # fig.update_coloraxes(colorbar_len=0.3)
    # fig.update_coloraxes(colorbar_tickfont=dict(color="#f4f4f4"))

    return fig


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
                                    className="card-title",
                                    style={'margin-bottom': '16px', }
                                    ),
                            html.P(
                        "       Esta plataforma busca responder"
                                " ¿cómo es la accesibilidad en Bogotá según el tipo de usuario?"
                                " En la sección de abajo encontrará menus para que juegue y vea"
                                "qué tan accesibles son las oportunidades para personas"
                                "según su modo de transporte",
                                className="card-text",
                            ),
                            html.H6('Seleccione un ciudad:'),
                            dcc.Dropdown(
                                options=list(constants.CENTER_CITY_COORDINATES.keys()),
                                value=list(constants.CENTER_CITY_COORDINATES.keys())[0],
                                id=constants.CITY_SELECTOR,
                                clearable=False,
                                style={'margin-bottom': '24px', }
                            ),
                            
                            html.H6('¿Qué desea ver?'),
                            dcc.RadioItems(
                                options=[
                                    {'label': ' Accesibilidad', 'value': 'ACC'},
                                    {'label': ' Población', 'value': 'POB'},
                                ],
                                value='ACC',
                                labelStyle={'margin-right': '12px', },
                                style={'margin-bottom': '12px', },
                                id=constants.CATEGORY_SELECTOR,
                            ),
                            
                            html.H6('  Seleccione una variable:'),
                            dcc.Dropdown(
                                #options=constants.CATEGORICAL_VARIABLES+constants.NON_CATEGORICAL_VARIABLES,
                                options=[
                                    # {'label': 'Nivel socioeconómico', 'value': 'NSE_5'},
                                    {'label': 'Índice de accesibilidad', 'value': 'IndiAcce'},
                                ],
                                value=constants.CATEGORICAL_VARIABLES[0],
                                id=constants.VARIABLE_SELECTOR,
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
                    dbc.Row(
                        children=[
                            html.Div(
                        # html.P("Seleccione un punto de la gráfica para ver los datos de una localidad.", className='graph-selector-text'),
                                children=
                                    [dcc.Graph(
                                        id=constants.SCATTER_ID,
                                        figure=get_bar_figure(),
                                        # figure=get_selector_graph(
                                        #     list(constants.CENTER_CITY_COORDINATES.keys())[0],
                                        #     list(constants.ACCESIBILITY_MEANS.keys())[0]
                                        # ),
                                        config={
                                            'displayModeBar': False
                                        },
                                        style={"height": "100%",
                                               "width": "95%"},
                                    )
                                ],
                                className='bar-content'
                            )
                        ],
                    ),
                ],
                className='map-container'
            ),
        ]
    ),
    ]
)



@app.callback(
        [
            Output(component_id=constants.VARIABLE_SELECTOR, component_property='options'),
            Output(component_id=constants.VARIABLE_SELECTOR, component_property='value'),
            Output(component_id=constants.MAP_ID, component_property='figure'),
        ],
    
        [
            Input(component_id=constants.CITY_SELECTOR, component_property='value'),
            Input(component_id=constants.CATEGORY_SELECTOR, component_property='value'),
            Input(component_id=constants.VARIABLE_SELECTOR, component_property='value')
            
        ],
        # Input(component_id=constants.ACCESIBILITY_SELECTOR,
        #       component_property='value'),
        # Input(component_id=constants.SCATTER_ID,
        #       component_property='hoverData'),
    
)
def update_output_div(city, category, variable):
    triggered_input = ctx.triggered_id
    if triggered_input == constants.CATEGORY_SELECTOR:
        if category == 'ACC':
            variable_options = [{'label': 'Índice de accesibilidad', 'value': 'IndiAcce'},]
            variable = constants.CATEGORICAL_VARIABLES[0]
        if category == 'POB':
            variable_options = [{'label': 'Nivel socioeconómico', 'value': 'NSE_5'},]
            variable = constants.CATEGORICAL_VARIABLES[1]
        return variable_options, variable, update_hex_map(city=city, fig_hex_map=fig_hex_map, variable=variable)
    return dash.no_update, dash.no_update, update_hex_map(city=city, fig_hex_map=fig_hex_map, variable=variable)
    






# Run the app
if __name__ == '__main__':
    app.run_server(
        debug=True,
        host='0.0.0.0', 
        port=8050
        )

