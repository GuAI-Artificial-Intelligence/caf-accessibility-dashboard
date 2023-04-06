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
from dash import Dash, dcc, html, Input, Output, State, ctx

# Bootstrap
import dash_bootstrap_components as dbc

# Local
import constants

# Credentials
from conf.credentials import MAPBOX_TOKEN

current_path = Path()


bogota_cuenca_df_csv = pd.read_csv(
    current_path / 'data' / 'bogota_cuenca_v1.csv')
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
        mapbox_center={
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

    if city == constants.BOGOTA_STR:
        zoom = 9.5

    if city == constants.CUENCA_STR:
        zoom = 11.5

    if nse_variable:
        colorbar = constants.CATEGORICAL_COLORBAR
        if variable == constants.CATEGORICAL_VARIABLES[0]:
            z = df[variable].map(constants.INDIACCE_DICTMAP).values
            colorbar['tickvals'] = constants.INDIACCE_TICKVALS
            colorbar['ticktext'] = constants.INDIACCE_TICKTEXT
            zmax = 4
            colorbar['title'] = '<b>Accesibilidad</b><br> .'
        if variable == constants.CATEGORICAL_VARIABLES[1]:
            z = df[variable].map(constants.NSE_5_DICTMAP).values
            colorbar['tickvals'] = constants.NS5_TICKVALS
            colorbar['ticktext'] = constants.NS5_TICKTEXT
            zmax = 5
            colorbar['title'] = '<b>Nivel socio<br>económico</b><br> .'
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
        mapbox_center={
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
    y1 = bogota_cuenca_df_csv[bogota_cuenca_df_csv.IndiAcce == '1. Alta'][[
        'NSE_5', 'Poblacion']].groupby('NSE_5').sum()['Poblacion'].values
    y2 = bogota_cuenca_df_csv[bogota_cuenca_df_csv.IndiAcce == '2. Media Alta'][[
        'NSE_5', 'Poblacion']].groupby('NSE_5').sum()['Poblacion'].values
    y3 = bogota_cuenca_df_csv[bogota_cuenca_df_csv.IndiAcce == '3. Media Baja'][[
        'NSE_5', 'Poblacion']].groupby('NSE_5').sum()['Poblacion'].values
    y4 = bogota_cuenca_df_csv[bogota_cuenca_df_csv.IndiAcce == '4. Baja'][[
        'NSE_5', 'Poblacion']].groupby('NSE_5').sum()['Poblacion'].values

    fig = go.Figure(data=[
        go.Bar(name='Baja', x=nse, y=y4, width=0.4, marker_color='#491874'),
        go.Bar(name='Media-Baja', x=nse, y=y3,
               width=0.4, marker_color='#a84276'),
        go.Bar(name='Media-Alta', x=nse, y=y2,
               width=0.4, marker_color='#eb8f6d'),
        go.Bar(name='Alta', x=nse, y=y1, width=0.4, marker_color='#fcfdc6'),
    ])

    fig.update_layout(
        xaxis_title="Nivel socioeconómico",
        yaxis_title="Habitantes",
        legend_title="  Accesibilidad",
        margin=dict(l=30, r=0, t=30, b=0),
        barmode='stack',
        paper_bgcolor='#323232',
        plot_bgcolor="#323232",
        font=dict(
            color="white"
        ),

    )

    return fig


# Create a Dash app
app = Dash(
    external_stylesheets=['assets/base.css', dbc.themes.BOOTSTRAP]
)
app.title = 'Accesibilidad'
app.layout = html.Div(
    [dbc.Row(
        children=[
            dbc.Col(
                width=4,
                className='panel-control-container',
                children=[
                    html.Div(
                        children=[
                            html.P('Accesibilidad en Bogotá y Cuenca',
                                   className='card-subtitle',
                                   style={'margin-bottom': '26px',
                                          'font-weight': 'bold', 'font-size': '14px'}
                                   ),
                            html.H5("¿Cómo es la accesibilidad en la ciudad según el tipo de usuario?",
                                    className="card-title",
                                    style={'margin-bottom': '12px',
                                           'font-size': '24px'}
                                    ),
                            html.P(
                                "Interactúe con las opciones de abajo y compruebe qué tan accesibles son las oportunidades para las personas.",
                                className="card-text",
                                style={'line-height': '1.2',
                                       'font-size': '15px', 'margin-bottom': '16px'}
                            ),
                            html.H6('Seleccione un ciudad:'),
                            dcc.Dropdown(
                                options=list(
                                    constants.CENTER_CITY_COORDINATES.keys()),
                                value=list(
                                    constants.CENTER_CITY_COORDINATES.keys())[0],
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
                                style={'margin-bottom': '16px', },
                                id=constants.CATEGORY_SELECTOR,
                            ),

                            html.H6('  Seleccione una variable:'),
                            dcc.Dropdown(
                                # options=constants.CATEGORICAL_VARIABLES+constants.NON_CATEGORICAL_VARIABLES,
                                options=[
                                    # {'label': 'Nivel socioeconómico', 'value': 'NSE_5'},
                                    {'label': 'Índice de accesibilidad',
                                        'value': 'IndiAcce'},
                                ],
                                value=constants.CATEGORICAL_VARIABLES[0],
                                id=constants.VARIABLE_SELECTOR,
                                clearable=False,
                                style={'margin-bottom': '50px', },
                            ),
                            dbc.Modal(
                                [
                                    dbc.ModalHeader(
                                        [
                                            dbc.Tabs(
                                                [
                                                    dbc.Tab(
                                                        label="Acerca de", tab_id="tab-1", className=""),
                                                    dbc.Tab(
                                                        label="Metodología", tab_id="tab-2", className="nav-link btn"),
                                                    dbc.Tab(
                                                        label="Espacio CAF", tab_id="tab-3", className="nav-link btn"),
                                                ],
                                                id="modal-tabs",
                                                active_tab="tab-1",
                                                className="my-tabs"
                                            )
                                        ]
                                    ),
                                    dbc.ModalBody(
                                        "This modal takes most of the vertical space of the page.",
                                        className="modal-body-scroll",
                                        id="modal-body"
                                    ),
                                    dbc.ModalFooter(
                                        dbc.Button("Cerrar", id="close",
                                                   className="ml-auto")
                                    ),
                                ],
                                id="modal",
                                size="xl",
                                backdrop=True,
                                className='modal-content'
                            ),
                            # dbc.Button("Ver notas", id="open", className='notes-button'),
                            html.A("Consulta la metodología", href="#", id="open-modal-link"),




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

                    html.Img(
                        src='assets/images/caf_tumi_numo_logos.png',
                        # style={'width':'75%', 'margin-left':'55px', 'margin-top':'50px', 'position':'absolute', 'bottom':'0px'}
                            style={'width': '100%', 'margin-left': '0px',
                                   'position': 'absolute', 'bottom': '0px'}
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
                                children=[dcc.Graph(
                                    id=constants.SCATTER_ID,
                                    figure=get_bar_figure(),
                                    # figure=get_selector_graph(
                                    #     list(constants.CENTER_CITY_COORDINATES.keys())[0],
                                    #     list(constants.ACCESIBILITY_MEANS.keys())[0]
                                    # ),
                                    config={
                                        'displayModeBar': False
                                    },
                                    style={"height": "94%",
                                           "width": "96%"},
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
        Output(component_id=constants.VARIABLE_SELECTOR,
               component_property='options'),
        Output(component_id=constants.VARIABLE_SELECTOR,
               component_property='value'),
        Output(component_id=constants.MAP_ID, component_property='figure'),
    ],

    [
        Input(component_id=constants.CITY_SELECTOR, component_property='value'),
        Input(component_id=constants.CATEGORY_SELECTOR,
              component_property='value'),
        Input(component_id=constants.VARIABLE_SELECTOR,
              component_property='value')

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
            variable_options = [
                {'label': 'Índice de accesibilidad', 'value': 'IndiAcce'},]
            variable = constants.CATEGORICAL_VARIABLES[0]
        if category == 'POB':
            variable_options = [
                {'label': 'Nivel socioeconómico', 'value': 'NSE_5'},]
            variable = constants.CATEGORICAL_VARIABLES[1]
        return variable_options, variable, update_hex_map(city=city, fig_hex_map=fig_hex_map, variable=variable)
    return dash.no_update, dash.no_update, update_hex_map(city=city, fig_hex_map=fig_hex_map, variable=variable)


# @app.callback(
#     Output("modal", "is_open"),
#     [Input("open", "n_clicks"), Input("close", "n_clicks")],
#     [State("modal", "is_open")],
# )
# def toggle_modal(n1, n2, is_open):
#     if n1 or n2:
#         return not is_open
#     return is_open


@app.callback(
    Output("modal", "is_open"),
    [Input("open-modal-link", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output("modal-body", "children"),
    [dash.dependencies.Input("modal-tabs", "active_tab")],
)
def render_tab_content(active_tab):
    if active_tab == "tab-1":
        return "Content of Acerca de"
    elif active_tab == "tab-2":
        return "Content of Metodologia"
    elif active_tab == "tab-3":
        return "Content of espacio CAF"
    else:
        return "Unknown tab selected"

# Run the app
if __name__ == '__main__':
    app.run_server(
        debug=True,
        host='0.0.0.0',
        port=8050
    )
