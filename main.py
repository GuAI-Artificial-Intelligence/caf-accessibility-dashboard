# Python
import json
from pathlib import Path
import os
import time

# Perfomance
from werkzeug.middleware.profiler import ProfilerMiddleware

# Data Analysis
import pandas as pd
import numpy as np

# Geo
import geopandas as gpd

# Plotly
import plotly.graph_objects as go
import plotly.express as px

# Dash
import dash
from dash import Dash, dcc, html, Input, Output, State, ctx
from dash.exceptions import PreventUpdate

# Bootstrap
import dash_bootstrap_components as dbc

# Local
import constants
import db


# Credentials
from conf.credentials import MAPBOX_TOKEN

current_path = Path()


# Data loading

accessibility_df, accessibility_geo = db.get_dataframe_from_sqlite_db(
    table_name='Accessibility', conn=db.conn)

# TODO
# TODO
# TODO
accessibility_df = gpd.read_file("temp_accesibilidad.geojson")
accessibility_geo = accessibility_df[["geometry"]].__geo_interface__
# TODO
# TODO

hospitales_df, hospitales_geo = db.get_dataframe_from_sqlite_db(
    table_name='Hospitals', conn=db.conn, geo_type='point')


espacios_verdes_df, espacios_verde_geo = db.get_dataframe_from_sqlite_db(
    table_name='Green_Areas', conn=db.conn)
espacios_verdes_df['name'].fillna(value='No disponible', inplace=True)


primary_health_care_df, primary_health_care_geo = db.get_dataframe_from_sqlite_db(
    table_name='Primary_Health_Care', conn=db.conn, geo_type='point')

primary_education_df, primary_education_geo = db.get_dataframe_from_sqlite_db(
    table_name='Primary_Education', conn=db.conn, geo_type='point')


early_education_df, early_education_geo = db.get_dataframe_from_sqlite_db(
    table_name='Early_Education', conn=db.conn, geo_type='point')


secondary_education_df, secondary_education_geo = db.get_dataframe_from_sqlite_db(
    table_name='Early_Education', conn=db.conn, geo_type='point')


# State variables
is_infra_trace_selected = False
is_population_trace_selected = False


def add_poblation_trace(fig, trace):
    # TODO
    # TODO
    # TODO
    # TODO
    # TODO
    # TODO
    # TODO

    global is_population_trace_selected
    global is_infra_trace_selected

    if is_infra_trace_selected:
        fig.data = fig.data[0:2]
    else:
        fig.data = fig.data[0:1]

    if trace == constants.TOT_POB_TRACE_NAME:
        is_population_trace_selected = False
        return fig

    is_population_trace_selected = True

    colorbar = constants.POPULATION_COLORBAR

    if trace == constants.BICIUSUARIO_TRACE_NAME:
        colorbar['title'] = '<b>Biciusuarios</b><br> .'
        var = "bicicleta"

    if trace == constants.PEATON_TRACE_NAME:
        colorbar['title'] = '<b>Peatones<br> .'
        var = "peaton"

    if trace == constants.MOVILIDAD_CUIDADO_TRACE_NAME:
        colorbar['title'] = '<b>Personas<br>con dificultad<br>para moverse<br> .'
        var = "movilidad_cuidado"

    trace = go.Densitymapbox(
        lat=accessibility_df.y,
        lon=accessibility_df.x,
        z=accessibility_df[var],
        name=constants.BICIUSUARIO_TRACE_NAME,
        radius=20,
        colorscale="Viridis",
        colorbar=colorbar,
        hoverinfo='skip'
    )

    fig = fig.add_trace(trace)

    return fig


def add_infraestructure_trace(fig, trace):

    global is_population_trace_selected
    global is_infra_trace_selected

    if is_population_trace_selected:
        fig.data = fig.data[0:2]
    else:
        fig.data = fig.data[0:1]

    if trace == constants.NONE_TRACE_NAME:
        is_infra_trace_selected = False
        return fig

    is_infra_trace_selected = True

    if trace == constants.HOSPITAL_TRACE_NAME:
        trace = go.Scattermapbox(
            lat=hospitales_geo.lat,
            lon=hospitales_geo.lon,
            mode="markers",
            marker=dict(
                size=10,
                color="#023e8a",
                symbol="hospital"
            ),
            name=constants.HOSPITAL_TRACE_NAME,
            customdata=hospitales_df[['nombre']],
            hovertemplate="<b>Nombre:</b> %{customdata[0]}",
        )

    if trace == constants.ATENCION_PRIMARIA_TRACE_NAME:
        trace = go.Scattermapbox(
            lat=primary_health_care_geo.lat,
            lon=primary_health_care_geo.lon,
            mode="markers",
            marker=dict(
                size=10,
                color="#0077b6",
                symbol="hospital"
            ),
            name=constants.ATENCION_PRIMARIA_TRACE_NAME,
            customdata=primary_health_care_df[['nombre']],
            hovertemplate="<b>Nombre:</b> %{customdata[0]}",
        )

    if trace == constants.EARLY_EDUCATION_TRACENAME:
        trace = go.Scattermapbox(
            lat=early_education_geo.lat,
            lon=early_education_geo.lon,
            mode="markers",
            marker=dict(
                size=10,
                # color="#9d4edd",
                symbol="college"
            ),
            name=constants.EARLY_EDUCATION_TRACENAME,
            customdata=early_education_df[['nombre', 'oferta']],
            hovertemplate="<b>Nombre:</b> %{customdata[0]}<br><b>Oferta:</b> %{customdata[1]}",
        )

    if trace == constants.PRIMARY_EDUCATION_TRACENAME:
        trace = go.Scattermapbox(
            lat=primary_education_geo.lat,
            lon=primary_education_geo.lon,
            mode="markers",
            marker=dict(
                size=10,
                # color="#7b2cbf"
                symbol="college"
            ),
            name=constants.PRIMARY_EDUCATION_TRACENAME,
            customdata=primary_education_df[['nombre', 'oferta']],
            hovertemplate="<b>Nombre:</b> %{customdata[0]}<br><b>Oferta:</b> %{customdata[1]}",
        )

    if trace == constants.SECONDARY_EDUCATION_TRACENAME:
        trace = go.Scattermapbox(
            lat=secondary_education_geo.lat,
            lon=secondary_education_geo.lon,
            mode="markers",
            marker=dict(
                size=10,
                # color="#5a189a",
                symbol="college"
            ),
            name=constants.SECONDARY_EDUCATION_TRACENAME,
            customdata=secondary_education_df[['nombre', 'oferta']],
            hovertemplate="<b>Nombre:</b> %{customdata[0]}<br><b>Oferta:</b> %{customdata[1]}",
        )

    if trace == constants.ESPACIOS_VERDES_TRACE_NAME:

        trace_gdf = espacios_verdes_df.copy()
        trace_gdf['z'] = 1

        trace = go.Choroplethmapbox(
            geojson=espacios_verde_geo,
            z=trace_gdf['z'].values,
            zmax=1,
            zmin=1,
            marker_line_width=0,
            locations=espacios_verdes_df.index.values.astype(str),
            colorbar=constants.HIDDEN_COLORBAR,
            colorscale=constants.HIDDEN_COLORSCALE,
            marker_opacity=0.5,
            customdata=espacios_verdes_df[['name']],
            hovertemplate="<b>Nombre:</b> %{customdata[0]}",
            name=constants.ESPACIOS_VERDES_TRACE_NAME
        )
        fig.update_layout(coloraxis_showscale=False)

    fig = fig.add_trace(trace)

    return fig


def init_map(df=accessibility_df, geodf=accessibility_geo,
             variable=constants.CATEGORICAL_VARIABLES[0], city=constants.BOGOTA_STR):
    z = df[variable].map(constants.INDIACCE_DICTMAP).values
    colorbar = constants.CATEGORICAL_COLORBAR
    colorbar['tickvals'] = constants.INDIACCE_TICKVALS
    colorbar['ticktext'] = constants.INDIACCE_TICKTEXT
    colorbar['title'] = '<b>Accesibilidad</b><br> .'

    fig_hex_map = go.Figure(
        go.Choroplethmapbox(
            geojson=geodf,
            z=z,
            locations=pd.Series(df.index.values).astype(str),
            colorbar=colorbar,
            colorscale=constants.INDIACCE_COLORSCALE,
            marker_opacity=0.5,
            customdata=df[['Poblacion', 'NSE_5',
                           constants.CATEGORICAL_VARIABLES[0]]],
            hovertemplate="<b>Habitantes:</b> %{customdata[0]}<br><b>Nivel socioeconómico:</b> '%{customdata[1]}'<br><b>Accesibilidad:</b> '%{customdata[2]}'",
            name=constants.MAP_TRACE_NAME
        )
    )

    fig_hex_map.update_layout(
        mapbox_accesstoken=MAPBOX_TOKEN,
        mapbox_center={
            "lat": constants.CENTER_CITY_COORDINATES[city]['center_lat'],
            "lon": constants.CENTER_CITY_COORDINATES[city]['center_lon']
        },
        mapbox_zoom=10,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    return fig_hex_map


def update_hex_map(city, fig_hex_map, variable=constants.CATEGORICAL_VARIABLES[0],
                   df=accessibility_df, filter={'all': True}, population="TOT_POB"):

    if not filter['all']:
        dfs = list()
        for nse in filter['selected']:
            mask = df[constants.CATEGORICAL_VARIABLES[1]] == nse
            mask = mask & df[constants.CATEGORICAL_VARIABLES[0]].isin(
                filter['selected'][nse])
            temp_df = df[mask]
            dfs.append(temp_df)
        df = pd.concat(dfs).copy()

    if (not population == constants.TOT_POB_TRACE_NAME) and (not filter["all"]):
        df = df[df[constants.MAP_BELOW_TAB_ACCESSIBILITY[population]] > 0].copy()

    lat = constants.CENTER_CITY_COORDINATES[city]['center_lat']
    lon = constants.CENTER_CITY_COORDINATES[city]['center_lon']

    cat_variable = False
    if variable in constants.CATEGORICAL_VARIABLES:
        cat_variable = True

    if city == constants.BOGOTA_STR:
        zoom = 10

    if city == constants.CUENCA_STR:
        zoom = 11.5

    colorscale = 'Brwnyl'

    if cat_variable:
        zmin = None
        zmax = None
        colorbar = constants.CATEGORICAL_COLORBAR
        if variable == constants.CATEGORICAL_VARIABLES[0]:
            z = df[variable].map(constants.INDIACCE_DICTMAP).values
            colorbar['tickvals'] = constants.INDIACCE_TICKVALS
            colorbar['ticktext'] = constants.INDIACCE_TICKTEXT
            colorbar['title'] = '<b>Accesibilidad</b><br> .'
            colorscale = constants.INDIACCE_COLORSCALE
            colorbar['tickmode'] = 'array'
        if variable == constants.CATEGORICAL_VARIABLES[1]:
            z = df[variable].map(constants.NSE_5_DICTMAP).values
            colorbar['tickvals'] = constants.NS5_TICKVALS
            colorbar['ticktext'] = constants.NS5_TICKTEXT
            colorbar['title'] = '<b>Nivel socio<br>económico</b><br> .'
            colorbar['tickmode'] = 'array'
    else:
        z = df[variable]
        z_city = df[df.city == city][variable]
        title = variable
        if "distance" in variable:
            title = "Distancia (km)"
        if "duration" in variable:
            title = "Tiempo (min)"
        colorbar = constants.CATEGORICAL_COLORBAR
        colorbar['title'] = f'<b>{title}</b><br> .'
        colorbar['tickmode'] = 'auto'
        zmin = z_city.quantile(0.0)
        zmax = z_city.quantile(0.9)

    fig_hex_map.update_traces(
        z=z,
        colorbar=colorbar,
        locations=pd.Series(df.index.values).astype(str),
        colorscale=colorscale,
        selector=dict(name=constants.MAP_TRACE_NAME),
        zmin=zmin,
        zmax=zmax,
    )

    fig_hex_map.update_layout(
        mapbox_center={
            "lat": lat,
            "lon": lon
        },
        mapbox_zoom=zoom,
    )

    return fig_hex_map


def get_bar_figure(fig_below_map=None, init=False, population=None, city="Bogotá", variable=constants.CATEGORICAL_VARIABLES[0]):

    if init:
        fig_below_map = go.Figure()

    if population is None:
        population = list(constants.POPULATION_TYPES.keys())[0]
        population_column = constants.MAP_BELOW_TAB_ACCESSIBILITY[population]
    else:
        population_column = constants.MAP_BELOW_TAB_ACCESSIBILITY[population]

    nse = list(constants.NSE_5_DICTMAP.keys())

    df = accessibility_df[accessibility_df.city == city]

    if variable in constants.CATEGORICAL_VARIABLES:

        y1 = df[df[constants.CATEGORICAL_VARIABLES[0]] == '1. Alta'][[
            'NSE_5', population_column]].groupby('NSE_5').sum()[population_column].values
        y2 = df[df[constants.CATEGORICAL_VARIABLES[0]] == '2. Media Alta'][[
            'NSE_5', population_column]].groupby('NSE_5').sum()[population_column].values
        y3 = df[df[constants.CATEGORICAL_VARIABLES[0]] == '3. Media Baja'][[
            'NSE_5', population_column]].groupby('NSE_5').sum()[population_column].values
        y4 = df[df[constants.CATEGORICAL_VARIABLES[0]] == '4. Baja'][[
            'NSE_5', population_column]].groupby('NSE_5').sum()[population_column].values

        fig_below_map.update(
            data=[
                go.Bar(
                    name='4. Baja', x=nse, y=y4, width=0.4, marker_color=constants.INDIACCE_COLORSCALE[0],
                    hoverinfo='none'
                ),

                go.Bar(
                    name='3. Media Baja', x=nse, y=y3, width=0.4, marker_color=constants.INDIACCE_COLORSCALE[1],
                    hoverinfo='none'
                ),
                go.Bar(
                    name='2. Media Alta', x=nse, y=y2, width=0.4, marker_color=constants.INDIACCE_COLORSCALE[2],
                    hoverinfo='none'
                ),
                go.Bar(
                    name='1. Alta', x=nse, y=y1, width=0.4, marker_color=constants.INDIACCE_COLORSCALE[3],
                    hoverinfo='none'
                ),
            ]
        )

        fig_below_map.update_layout(
            xaxis_title="Nivel socioeconómico",
            yaxis_title="Número de personas",
            legend_title="  Accesibilidad",
            margin=dict(l=30, r=0, t=30, b=0),
            barmode='stack',
            paper_bgcolor='#323232',
            plot_bgcolor="#323232",
            font=dict(
                color="white"
            ),
            dragmode='select',
        )
    else:

        y1 = df[df.NSE_5 ==
                '1 - Alto'][variable].values
        y2 = df[df.NSE_5 ==
                '2 - Medio-Alto'][variable].values
        y3 = df[df.NSE_5 ==
                '3 - Medio'][variable].values
        y4 = df[df.NSE_5 ==
                '4 - Medio-Bajo'][variable].values
        y5 = df[df.NSE_5 ==
                '5 - Bajo'][variable].values

        fig_below_map.update(
            data=[
                go.Box(
                    y=y1, name='1 - Alto', boxpoints='all',
                ),
                go.Box(
                    y=y2, name='2 - Medio-Alto', boxpoints='all',
                ),
                go.Box(
                    y=y3, name='3 - Medio', boxpoints='all',
                ),
                go.Box(
                    y=y4, name='4 - Medio-Bajo', boxpoints='all',
                ),
                go.Box(
                    y=y5, name='5 - Bajo', boxpoints='all',
                ),
            ]
        )

        title = "Distancia (km)"
        if "duration" in variable:
            title = "Tiempo (minutos)"

        fig_below_map.update_layout(
            xaxis_title="Nivel socioeconómico",
            yaxis_title=title,
            showlegend=False,
            margin=dict(l=30, r=0, t=30, b=0),
            paper_bgcolor='#323232',
            plot_bgcolor="#323232",
            font=dict(
                color="white"
            ),
            dragmode='select'
        )

    return fig_below_map


fig_hex_map = init_map()
fig_below_map = get_bar_figure(init=True)


# Create a Dash app
app = Dash(
    __name__,
    external_stylesheets=[
        'assets/base.css',
        dbc.themes.BOOTSTRAP,  dbc.icons.BOOTSTRAP
    ],
)

app.title = 'CAF - Accesibilidad'


left_panel_content = [

    html.Img(
        src='assets/images/caf_tumi_numo_logos.png',
        style={
            'width': "calc(100%)",
            'margin-left': '-24px',
            'bottom': '0',
            "position": 'absolute',
        }
    ),

    html.P('Accesibilidad en Bogotá y Cuenca',
           className='card-subtitle',
           style={'margin-bottom': '16px', 'margin-top': '26px',
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
        style={'margin-bottom': '10px', }
    ),

    html.H6('¿Qué desea ver?'),
    dbc.RadioItems(
        options=[
            {'label': ' Accesibilidad',
             'value': 'ACC'},
            {'label': ' Población',
             'value': 'POB'},
        ],
        value='ACC',
        className="btn-group",
        inputClassName="btn-check",
        labelClassName="btn btn-outline-primary btn-sm",
        labelCheckedClassName="active",
        style={'margin-bottom': '16px', },
        id=constants.CATEGORY_SELECTOR,
    ),

    html.H6('  Seleccione un modo de transporte:'),
    dcc.Dropdown(
        options=constants.TRANSPORT_MODES,
        value=constants.TRANSPORT_MODES[0],
        id=constants.TRANSPORT_MODE_SELECTOR,
        clearable=False,
        style={'margin-bottom': '10px', },
    ),

    html.H6('  Seleccione una variable:'),
    dcc.Dropdown(
        options=[
            {'label': 'Índice de accesibilidad',
             'value': constants.CATEGORICAL_VARIABLES[0]},
        ],
        value=constants.CATEGORICAL_VARIABLES[0],
        id=constants.VARIABLE_SELECTOR,
        clearable=False,
        style={'margin-bottom': '10px', },
    ),
    html.H6(
        '¿Qué establecimientos desea ver?'),
    dcc.Dropdown(
        id=constants.INFRA_SELECTOR,
        options=constants.INFRA_TYPES,
        clearable=False,
        style={'margin-bottom': '10px', },
        value=constants.NONE_TRACE_NAME,
    ),

    html.H6(
        'Seleccione un tipo de población:'),
    dcc.Dropdown(
        id=constants.POPULATION_TYPE_SELECTOR,
        # options=[
        #     {"label": constants.POPULATION_TYPES[value], "value": value} for value in constants.POPULATION_TYPES
        # ],
        options=constants.POPULATION_TYPES,
        value=constants.TOT_POB_TRACE_NAME,
        clearable=False,
    ),



    dbc.Modal(
        [
            dbc.ModalHeader(
                [
                    dbc.Tabs(
                        [
                            dbc.Tab(
                                label="Acerca de", tab_id="tab-1", className="nav-link"),
                            dbc.Tab(
                                label="Metodología", tab_id="tab-2", className="nav-link"),
                            dbc.Tab(
                                label="Proyecto TUMI Data Hub", tab_id="tab-3", className="nav-link"),
                        ],
                        id="modal-tabs",
                        active_tab="tab-1",
                        className="my-tabs"
                    )
                ],
                style={'margin-left': '50px'}
            ),
            dbc.ModalBody(
                "This modal takes most of the vertical space of the page.",
                className="modal-body-scroll",
                id="modal-body"
            ),
            dbc.ModalFooter(
                dbc.Button("Cerrar", id="close",
                           className="ml-auto", style={'background-color': 'rgb(72, 155, 248)'})
            ),
        ],
        id="modal",
        size="xl",
        backdrop=True,
        className='modal-content',
    ),



]

map_layout = [
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
    )
]

bottom_graph_layout = [
    html.Div(
        children=[
            dcc.Graph(
                id=constants.BELOW_GRAPH,
                figure=fig_below_map,
                config={
                    'displayModeBar': False
                },
                style={"height": "94%",
                       "width": "96%",
                       'margin-top': '0px',
                       },
            ),

        ],
        className='bar-content',
    )
]

selector_panel_layout = [

    dbc.Button(
        children=[
            html.I(
                className="bi bi-arrow-left-right",
                style={
                    "padding": "0px",
                    "marging-right": "0px",
                }
            ),
        ],
        id="hide-show-left-panel",
        style={
            "background-color": "rgb(30,30,30)",
            "color": "white",
            "border": "none",
            "width": "32px",
            "height": "32px",
            "margin-top": "16px",
            "display": "flex", "justify-content": "center", "align-items": "center",
        },
    ),
    dbc.Button(
        children=[
            html.I(
                className="bi bi-patch-question-fill",
                style={
                    "padding": "0px",
                    "marging-right": "0px",
                }
            ),
        ],
        id="open-modal-link",
        style={
            "background-color": "rgb(30,30,30)",
            "color": "white",
            "border": "none",
            "width": "32px",
            "height": "32px",
            "margin-top": "16px",
            "display": "flex", "justify-content": "center", "align-items": "center",
        },
    )
]


below_graph_control_panel = [
    # TODO
    # TODO
    # TODO
    # html.Div(
    #     id="below-graph-control-panel",
    #     children=[
    #         dcc.Dropdown(
    #             id=constants.BELOW_TABS,
    #             options=[
    #                 {"label": constants.POPULATION_TYPES[value], "value": value} for value in constants.POPULATION_TYPES
    #             ],
    #             value=list(constants.POPULATION_TYPES.keys())[0],
    #             clearable=False,
    #             style={
    #                 "width": "calc(300px)",
    #                 "margin-left": "16px",
    #             }
    #         ),
    #     ]
    # ),
    # TODO
    # TODO
    # TODO


    dbc.Button(
        children=[
            html.I(
                className="bi bi-arrow-down-up",
                style={
                    "padding": "0px",
                    "marging-right": "0px",
                }
            ),
        ],
        id=constants.HIDE_SHOW_BOTTOM_GRAPH_PANEL,
        style={
            "background-color": "rgb(30,30,30)",
            "color": "white",
            "border": "none",
            "width": "32px",
            "height": "32px",
            "margin-right": "32px",
            "display": "flex", "justify-content": "center", "align-items": "center",
            "margin-left": "auto",

        },
    )
]


app.layout = html.Div(

    children=[
        html.Div(
            children=[
                html.Div(
                    children=selector_panel_layout,
                    style={
                        "width": "3%", "height": "100vh",
                        "background-color": "rgb(30, 30, 30)",
                        "display": "flex", "flex-direction": "column",
                        "align-items": "center", "border-right": "0.1px solid rgba(255,255,255,0.2)",
                    },
                    id='selector-panel'
                ),
                html.Div(
                    children=left_panel_content,
                    style={"width": "30%", "height": "100vh",
                           "padding": "24px 30px 0px 30px", "position": "relative",
                           'overflow': 'scroll',
                           'overflowX': 'hidden',
                           },
                    id='left-panel',
                    className='panel-control-content'
                ),

                html.Div(
                    children=[
                        dcc.Loading(
                            children=[
                                html.Div(
                                    children=map_layout,
                                    id=constants.MAP_PANEL,
                                    style={"width": "100%",
                                           "height": "96vh", },
                                ),

                                html.Div(
                                    children=below_graph_control_panel,
                                    style={
                                        "width": "100%", "height": "4vh",
                                        "background-color": "rgb(30, 30, 30)",
                                        "display": "flex",
                                        "align-items": "center",
                                    }
                                ),
                                html.Div(
                                    children=bottom_graph_layout,
                                    id=constants.BOTTOM_GRAPH_PANEL,
                                    style={"width": "100%",
                                           "display": "none", "height": "0vh"},
                                ),]
                        )



                    ],
                    style={"width": "68%", "height": "100vh", },
                    id='right-panel',
                    className='map-container'
                )


            ],
            style={"display": "flex"},
            id='main-container'
        )
    ]
)


@app.callback(
    [
        Output(constants.MAP_PANEL, 'style'),
        Output(constants.BOTTOM_GRAPH_PANEL, 'style'),
    ],
    [
        Input(constants.HIDE_SHOW_BOTTOM_GRAPH_PANEL, 'n_clicks')
    ]
)
def hide_show_left_panel(n_clicks):
    if n_clicks is None:
        return dash.no_update, dash.no_update
    if n_clicks % 2 == 0:
        return {"width": "100%", "height": "96vh", }, {"width": "100%", "height": "0vh", "display": "none"}
    else:
        return {"width": "100%", "height": "60vh", }, {"width": "100%", "height": "35vh", "display": "flex"}


@app.callback(
    [
        Output('left-panel', 'style'),
        Output('right-panel', 'style'),
    ],
    [
        Input('hide-show-left-panel', 'n_clicks')
    ]
)
def hide_show_left_panel(n_clicks):
    if n_clicks is None:
        return dash.no_update, dash.no_update

    if n_clicks % 2 == 0:
        return {'overflow': 'scroll', "width": "30%", "height": "100vh", "padding": "24px 40px 0px 24px", "display": "flex", "position": "relative"}, {"width": "68%", "height": "100vh",
                                                                                                                                                       "background-color": "#323232"}
    else:
        return {"width": "0%", "height": "100vh", "padding": "0px", "display": "none"}, {"width": "98%", "height": "100vh",
                                                                                         "background-color": "#323232"}


@app.callback(
    [
        Output(component_id=constants.VARIABLE_SELECTOR,
               component_property='options'),
        Output(component_id=constants.VARIABLE_SELECTOR,
               component_property='value'),
        Output(component_id=constants.MAP_ID, component_property='figure'),
        Output(component_id=constants.BELOW_GRAPH,
               component_property='figure'),
        Output(constants.TRANSPORT_MODE_SELECTOR, 'disabled'),
        Output(constants.TRANSPORT_MODE_SELECTOR, 'value'),
        Output(constants.POPULATION_TYPE_SELECTOR, 'options')
    ],

    [
        Input(component_id=constants.CITY_SELECTOR, component_property='value'),
        Input(component_id=constants.CATEGORY_SELECTOR,
              component_property='value'),
        Input(component_id=constants.VARIABLE_SELECTOR,
              component_property='value'),
        Input(constants.BELOW_GRAPH, 'selectedData'),
        Input(constants.POPULATION_TYPE_SELECTOR, 'value'),
        Input(constants.TRANSPORT_MODE_SELECTOR, 'value'),
        Input(constants.INFRA_SELECTOR, 'value'),
    ],

)
def update_output_div(city,
                      category,
                      variable,
                      below_graph_selected_data,
                      population_type_selection,
                      transport_mode_selection,
                      infra_selection):
    triggered_input = ctx.triggered_id

    if triggered_input is None:
        raise PreventUpdate

    if triggered_input == constants.CITY_SELECTOR:
        if city == "Bogotá":
            options = [
                {"label": constants.POPULATION_TYPES[value], "value": value} for value in constants.POPULATION_TYPES
            ]
        if city == "Cuenca":
            options = [
                {"label": constants.POPULATION_TYPES["TOT_POB"],
                    "value": "TOT_POB"}
            ]
        return (dash.no_update,
                dash.no_update,
                update_hex_map(city=city, fig_hex_map=fig_hex_map, variable=variable,
                               population=population_type_selection),
                get_bar_figure(
                    fig_below_map=fig_below_map,population=population_type_selection, city=city, variable=variable),
                dash.no_update,
                dash.no_update,
                options)

    transport_mode_disabled = False

    if triggered_input == constants.POPULATION_TYPE_SELECTOR:

        map_fig = add_poblation_trace(
            fig=fig_hex_map, trace=population_type_selection)

        bar_graph = get_bar_figure(
            fig_below_map=fig_below_map,population=population_type_selection, city=city, variable=variable)

        return (dash.no_update,
                dash.no_update,
                map_fig,
                bar_graph,
                transport_mode_disabled,
                dash.no_update,
                dash.no_update)

    if triggered_input == constants.INFRA_SELECTOR:

        map_fig = add_infraestructure_trace(fig_hex_map, infra_selection)

        return (dash.no_update,
                dash.no_update,
                map_fig,
                dash.no_update,
                transport_mode_disabled,
                dash.no_update,
                dash.no_update)

    if (triggered_input == constants.BELOW_GRAPH):

        if below_graph_selected_data is None:
            nse_selection = {
                'all': True,
            }

        elif (len(below_graph_selected_data["points"]) > 0):
            nse_selection = {
                'all': False,
                'selected': dict()
            }
            if transport_mode_selection == constants.TRANSPORT_MODES[0]:

                for selection in below_graph_selected_data['points']:

                    accesibilidad = fig_below_map['data'][selection['curveNumber']]['name']
                    nse = selection['x']
                    if nse not in nse_selection['selected']:
                        nse_selection['selected'][nse] = set()
                    nse_selection['selected'][nse].add(accesibilidad)

            elif transport_mode_selection in constants.TRANSPORT_MODES[1:]:
                curves = set()
                for selection in below_graph_selected_data['points']:
                    curves.add(selection['curveNumber'])
                curve_nse_map = {
                    0: "1 - Alto",
                    1: "2 - Medio-Alto",
                    2: "3 - Medio",
                    3: "4 - Medio-Bajo",
                    4: "5 - Bajo",
                }
                for curve in curves:
                    nse = curve_nse_map[curve]
                    nse_selection['selected'][nse] = {
                        '1. Alta', '2. Media Alta', '3. Media Baja', '4. Baja'}

        elif len(below_graph_selected_data["points"]) == 0:
            raise PreventUpdate
        else:
            nse_selection = {
                'all': True,
            }

        return (dash.no_update,
                dash.no_update,
                update_hex_map(city=city, fig_hex_map=fig_hex_map, variable=variable, filter=nse_selection,
                               population=population_type_selection),
                get_bar_figure(
                    fig_below_map=fig_below_map,population=population_type_selection, city=city, variable=variable),
                transport_mode_disabled,
                dash.no_update,
                dash.no_update)

    if triggered_input == constants.CATEGORY_SELECTOR:
        if category == 'ACC':
            variable_options = [
                {'label': 'Índice de accesibilidad', 'value': constants.CATEGORICAL_VARIABLES[0]},]
            variable = constants.CATEGORICAL_VARIABLES[0]
        if category == 'POB':
            variable_options = [
                {'label': 'Nivel socioeconómico', 'value': 'NSE_5'},]
            variable = constants.CATEGORICAL_VARIABLES[1]
            transport_mode_disabled = True

        return (variable_options,
                variable,
                update_hex_map(city=city, fig_hex_map=fig_hex_map,
                               variable=variable, population=population_type_selection),
                get_bar_figure(population=population_type_selection,
                               city=city, variable=variable),
                transport_mode_disabled,
                constants.TRANSPORT_MODES[0],
                dash.no_update)

    if triggered_input == constants.TRANSPORT_MODE_SELECTOR:

        if transport_mode_selection == "A pie":
            variable_options = constants.VARIABLE_OPTIONS_FOOT
            variable = variable_options[0]["value"]

        elif transport_mode_selection == "Bicicleta":
            variable_options = constants.VARIABLE_OPTIONS_BYCICLE
            variable = variable_options[0]["value"]

        elif transport_mode_selection == "Carro":
            variable_options = constants.VARIABLE_OPTIONS_CAR
            variable = variable_options[0]["value"]

        elif transport_mode_selection == "Todos":
            variable_options = [
                {'label': 'Índice de accesibilidad', 'value': constants.CATEGORICAL_VARIABLES[0]},]
            variable = constants.CATEGORICAL_VARIABLES[0]

        return (variable_options,
                variable,
                update_hex_map(city=city, fig_hex_map=fig_hex_map,
                               variable=variable, population=population_type_selection),
                get_bar_figure(fig_below_map=fig_below_map,population=population_type_selection,
                               city=city, variable=variable),
                transport_mode_disabled,
                dash.no_update,
                dash.no_update)

    return (dash.no_update,
            dash.no_update,
            update_hex_map(city=city, fig_hex_map=fig_hex_map,
                           variable=variable, population=population_type_selection),
            get_bar_figure(fig_below_map=fig_below_map,population=population_type_selection,
                           city=city, variable=variable),
            transport_mode_disabled,
            dash.no_update,
            dash.no_update)


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
    Output("modal-body", "children"),
    [Input("modal-tabs", "active_tab")],
)
def render_tab_content(active_tab):
    if active_tab == "tab-1":
        return constants.ACERCA_DE_BODY_CONTENT
    elif active_tab == "tab-2":
        return constants.ACERCA_DE_BODY_METODOLOGIA
    elif active_tab == "tab-3":
        return constants.ESPACIO_CAF_BODY_METODOLOGIA
    else:
        return "Unknown tab selected"


PROF_DIR = current_path / 'profile'

if __name__ == "__main__":
    if os.getenv("PROFILER", None):
        app.server.config["PROFILE"] = True
        app.server.wsgi_app = ProfilerMiddleware(
            app.server.wsgi_app,
            sort_by=["cumtime"],
            restrictions=[50],
            stream=None,
            profile_dir=PROF_DIR
        )
    app.run_server(debug=True)
