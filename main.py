# Python
import json
from pathlib import Path
import time
import sys


# Data Analysis
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.ops import unary_union

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


bogota_cuenca_df_parquet = pd.read_parquet(
    current_path / 'data' / 'bogota_cuenca_v2.parquet'
)

bogota_cuenca_gdf_geo = gpd.read_parquet(
    current_path / 'data' / 'bogota_cuenca_geo_v2.parquet',
)

hospitales_gdf = gpd.read_parquet(
    current_path / 'data' / 'Bogota_SaluHosp.parquet'
)

espacios_verdes_gdf = gpd.read_parquet(
    current_path / 'data' / 'Bogota_EspaVerd.parquet'
)
espacios_verdes_gdf['name'].fillna(value='No disponible', inplace=True)


def add_infraestructure_trace(fig, infra_traces):
    new_traces = [trace for trace in fig.data if trace['name']
                  == constants.MAP_TRACE_NAME]
    if len(infra_traces) != 0:
        for i, value in enumerate(infra_traces):

            if value == constants.HOSPITAL_TRACE_NAME:
                trace = go.Scattermapbox(
                    lat=hospitales_gdf.geometry.y,
                    lon=hospitales_gdf.geometry.x,
                    mode="markers",
                    marker=dict(
                        size=5,
                        color="blue"
                    ),
                    name=constants.HOSPITAL_TRACE_NAME,
                    customdata=hospitales_gdf[['nombre']],
                    hovertemplate="<b>Nombre:</b> %{customdata[0]}",
                )
            if value == constants.ESPACIOS_VERDES_TRACE_NAME:
                trace_gdf = espacios_verdes_gdf.copy()
                trace_gdf['z'] = 1
                trace = go.Choroplethmapbox(
                    geojson=json.loads(espacios_verdes_gdf.geometry.to_json()),
                    z=trace_gdf['z'].values,
                    zmax=1,
                    zmin=1,
                    marker_line_width=0,
                    locations=espacios_verdes_gdf.index.values.astype(str),
                    colorbar=constants.HIDDEN_COLORBAR,
                    colorscale=constants.HIDDEN_COLORSCALE,
                    marker_opacity=0.5,
                    customdata=espacios_verdes_gdf[['name']],
                    hovertemplate="<b>Nombre:</b> %{customdata[0]}",
                    name=constants.ESPACIOS_VERDES_TRACE_NAME
                )
                fig.update_layout(coloraxis_showscale=False)

            new_traces.append(trace)

    return fig.update(data=new_traces, overwrite=True)


def init_map(df=bogota_cuenca_df_parquet, geodf=bogota_cuenca_gdf_geo.geometry, variable=constants.CATEGORICAL_VARIABLES[0], city=constants.BOGOTA_STR):
    z = df[variable].map(constants.INDIACCE_DICTMAP).values
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
        mapbox_zoom=9.5,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    return fig_hex_map


fig_hex_map = init_map()
fig_below_map = go.Figure()

# add_infraestructure_trace(hospitales_gdf, fig_hex_map)

# end_time2 = time.time()

# elapsed_time = end_time - start_time
# elapsed_time2 = end_time2 - start_time2
# print(f"Elapsed time (2): {elapsed_time} seconds")
# print(f"Elapsed time (3): {elapsed_time2} seconds")


def update_hex_map(city, fig_hex_map, variable=constants.CATEGORICAL_VARIABLES[0],
                   df=bogota_cuenca_df_parquet, filter={'all': True},
                   geodf=bogota_cuenca_gdf_geo):

    if not filter['all']:
        dfs = list()
        for nse in filter['selected']:
            mask = df[constants.CATEGORICAL_VARIABLES[1]] == nse
            mask = mask & df[constants.CATEGORICAL_VARIABLES[0]].isin(
                filter['selected'][nse])
            temp_df = df[mask]
            dfs.append(temp_df)
        df = pd.concat(dfs).copy()
        geodf = geodf[geodf.hex.isin(df.hex)].copy()
        geodf = geodf.geometry

    lat = constants.CENTER_CITY_COORDINATES[city]['center_lat']
    lon = constants.CENTER_CITY_COORDINATES[city]['center_lon']

    nse_variable = False
    if variable in constants.CATEGORICAL_VARIABLES:
        nse_variable = True

    if city == constants.BOGOTA_STR:
        zoom = 9.5

    if city == constants.CUENCA_STR:
        zoom = 11.5

    colorscale = 'Brwnyl'

    if nse_variable:
        colorbar = constants.CATEGORICAL_COLORBAR
        if variable == constants.CATEGORICAL_VARIABLES[0]:
            z = df[variable].map(constants.INDIACCE_DICTMAP).values
            colorbar['tickvals'] = constants.INDIACCE_TICKVALS
            colorbar['ticktext'] = constants.INDIACCE_TICKTEXT
            zmax = 4
            colorbar['title'] = '<b>Accesibilidad</b><br> .'
            colorscale = constants.INDIACCE_COLORSCALE
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

    trace = go.Choroplethmapbox(
        geojson=json.loads(geodf.to_json()),
        z=z,
        # zmin=0,
        # zmax=zmax,
        locations=pd.Series(df.index.values).astype(str),
        colorbar=colorbar,
        colorscale=colorscale,
        marker_opacity=0.5,
        customdata=df[['Poblacion', 'NSE_5',
                       constants.CATEGORICAL_VARIABLES[0]]],
        hovertemplate="<b>Habitantes:</b> %{customdata[0]}<br><b>Nivel socioeconómico:</b> '%{customdata[1]}'<br><b>Accesibilidad:</b> '%{customdata[2]}'",
        name=constants.MAP_TRACE_NAME
    )
    data = list(fig_hex_map.data)
    data[0] = trace
    fig_hex_map.update(data=data, overwrite=True)

    # fig_hex_map.update_traces(
    #     geojson=json.loads(geodf.to_json()),
    #     overwrite=True,
    #     z=z,
    #     zmin=0,
    #     zmax=zmax,
    #     colorscale=colorscale,
    #     colorbar=colorbar,
    #     selector=dict(type='choroplethmapbox'),
    #     customdata=df[['Poblacion', 'NSE_5', 'IndiAcce_1']],
    #     hovertemplate="<b>Habitantes:</b> %{customdata[0]}<br><b>Nivel socioeconómico:</b> %{customdata[1]}<br><b>Accesibilidad:</b> %{customdata[2]}",
    # )

    fig_hex_map.update_layout(
        mapbox_center={
            "lat": lat,
            "lon": lon
        },
        mapbox_zoom=zoom,
    )

    return fig_hex_map


def get_bar_figure():

    nse = bogota_cuenca_df_parquet.NSE_5.unique()
    nse = [
        '1 - Alto',
        '2 - Medio-Alto',
        '3 - Medio',
        '4 - Medio-Bajo',
        '5 - Bajo'
    ]
    y1 = bogota_cuenca_df_parquet[bogota_cuenca_df_parquet[constants.CATEGORICAL_VARIABLES[0]] == '1. Alta'][[
        'NSE_5', 'Poblacion']].groupby('NSE_5').sum()['Poblacion'].values
    y2 = bogota_cuenca_df_parquet[bogota_cuenca_df_parquet[constants.CATEGORICAL_VARIABLES[0]] == '2. Media Alta'][[
        'NSE_5', 'Poblacion']].groupby('NSE_5').sum()['Poblacion'].values
    y3 = bogota_cuenca_df_parquet[bogota_cuenca_df_parquet[constants.CATEGORICAL_VARIABLES[0]] == '3. Media Baja'][[
        'NSE_5', 'Poblacion']].groupby('NSE_5').sum()['Poblacion'].values
    y4 = bogota_cuenca_df_parquet[bogota_cuenca_df_parquet[constants.CATEGORICAL_VARIABLES[0]] == '4. Baja'][[
        'NSE_5', 'Poblacion']].groupby('NSE_5').sum()['Poblacion'].values

    # fig = go.Figure(
    #     data=[
    #         go.Bar(
    #             name='Baja', x=nse, y=y4, width=0.4, marker_color=constants.INDIACCE_COLORSCALE[0],
    #             hoverinfo='none'
    #         ),

    #         go.Bar(
    #             name='Media-Baja', x=nse, y=y3, width=0.4, marker_color=constants.INDIACCE_COLORSCALE[1],
    #             hoverinfo='none'
    #         ),
    #         go.Bar(
    #             name='Media-Alta', x=nse, y=y2, width=0.4, marker_color=constants.INDIACCE_COLORSCALE[2],
    #             hoverinfo='none'
    #         ),
    #         go.Bar(
    #             name='Alta', x=nse, y=y1, width=0.4, marker_color=constants.INDIACCE_COLORSCALE[3],
    #             hoverinfo='none'
    #         ),
    #     ],
    # )

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
        yaxis_title="Habitantes",
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

    return fig_below_map



# Create a Dash app
app = Dash(
    __name__,
    external_stylesheets=['assets/base.css',
                          dbc.themes.BOOTSTRAP,  dbc.icons.BOOTSTRAP],
)

app.title = 'Accesibilidad'

app.layout = dcc.Loading(
    type='graph',
    children=[dbc.Row(
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
                            dbc.RadioItems(
                                options=[
                                    {'label': ' Accesibilidad', 'value': 'ACC'},
                                    {'label': ' Población', 'value': 'POB'},
                                ],
                                value='ACC',
                                className="btn-group",
                                inputClassName="btn-check",
                                labelClassName="btn btn-outline-primary btn-sm",
                                labelCheckedClassName="active",
                                style={'margin-bottom': '16px', },
                                id=constants.CATEGORY_SELECTOR,
                            ),

                            html.H6('  Seleccione una variable:'),
                            dcc.Dropdown(
                                # options=constants.CATEGORICAL_VARIABLES+constants.NON_CATEGORICAL_VARIABLES,
                                options=[
                                    # {'label': 'Nivel socioeconómico', 'value': 'NSE_5'},
                                    {'label': 'Índice de accesibilidad',
                                     'value': constants.CATEGORICAL_VARIABLES[0]},
                                ],
                                value=constants.CATEGORICAL_VARIABLES[0],
                                id=constants.VARIABLE_SELECTOR,
                                clearable=False,
                                style={'margin-bottom': '20px', },
                            ),
                            html.H6('¿Qué establecimientos desea ver?'),
                            dcc.Checklist(
                                options=[
                                    {'label': ' Hospitales',
                                        'value': constants.HOSPITAL_TRACE_NAME},
                                    {'label': ' Espacios verdes',
                                        'value': constants.ESPACIOS_VERDES_TRACE_NAME},
                                    # {'label': ' Option 3', 'value': 3}
                                ],
                                labelStyle={'margin-right': '12px'},
                                style={'margin-bottom': '50px', },
                                id=constants.INFRA_CHECKLIST_ID
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
                            # dbc.Button("Sobre este tablero", id="open", className='notes-button btn-dark'),

                            html.A(children=[
                                html.I(
                                    className="bi bi-patch-question-fill me-2"),
                                "Sobre este tablero"
                            ],
                                href="#", id="open-modal-link",
                            ),


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
                                children=[
                                    dcc.Graph(
                                        id=constants.SCATTER_ID,
                                        figure=get_bar_figure(),
                                        config={
                                            'displayModeBar': False
                                        },
                                        style={"height": "94%",
                                               "width": "96%",
                                               'margin-top': '26px',
                                               },
                                    ),
                                    dbc.RadioItems(
                                        id="radios",
                                        className="btn-group",
                                        inputClassName="btn-check",
                                        labelClassName="btn btn-outline-primary btn-sm",
                                        labelCheckedClassName="active",
                                        options=[
                                            {"label": "Nivel socieconómico",
                                                "value": 1},
                                            {"label": "Option 2", "value": 2},
                                            # {"label": "Option 3", "value": 3},
                                        ],
                                        value=1,
                                        style={
                                            # 'width': '200px',
                                            'position': 'absolute',
                                            'top': 0,
                                            'left': 0,
                                            'z-index': 10,
                                            'margin-top': '12px',
                                            'background-color': '#323232',

                                        },

                                    ),


                                ],
                                className='bar-content',
                                style={'position': 'relative'}
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
              component_property='value'),
        Input(constants.SCATTER_ID, 'selectedData'),
        Input(constants.INFRA_CHECKLIST_ID, 'value'),

    ],

)
def update_output_div(city, category, variable, belowGraphSelectedData, infra_checklist):
    triggered_input = ctx.triggered_id

    # time.sleep(200)

    if triggered_input is None:
        return dash.no_update, dash.no_update, dash.no_update

    if triggered_input == constants.INFRA_CHECKLIST_ID:
        map_fig = add_infraestructure_trace(fig_hex_map, infra_checklist)

        return dash.no_update, dash.no_update, map_fig

    if (triggered_input == constants.SCATTER_ID):
        if (belowGraphSelectedData is not None):
            nse_selection = {
                'all': False,
                'selected': dict()
            }
            for selection in belowGraphSelectedData['points']:
                accesibilidad = fig_below_map['data'][selection['curveNumber']]['name']
                nse = selection['x']
                if nse not in nse_selection['selected']:
                    nse_selection['selected'][nse] = set()
                nse_selection['selected'][nse].add(accesibilidad)
        else:
            nse_selection = {
                'all': True,
            }

        return dash.no_update, dash.no_update, update_hex_map(
            city=city, fig_hex_map=fig_hex_map, variable=variable, filter=nse_selection)

    if triggered_input == constants.CATEGORY_SELECTOR:
        if category == 'ACC':
            variable_options = [
                {'label': 'Índice de accesibilidad', 'value': constants.CATEGORICAL_VARIABLES[0]},]
            variable = constants.CATEGORICAL_VARIABLES[0]
        if category == 'POB':
            variable_options = [
                {'label': 'Nivel socioeconómico', 'value': 'NSE_5'},]
            variable = constants.CATEGORICAL_VARIABLES[1]
        if category == 'INFRA':

            return dash.no_update, dash.no_update, dash.no_update

        return variable_options, variable, update_hex_map(city=city, fig_hex_map=fig_hex_map, variable=variable)

    return dash.no_update, dash.no_update, update_hex_map(city=city, fig_hex_map=fig_hex_map, variable=variable)


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
        return constants.ACERCA_DE_BODY_CONTENT
    elif active_tab == "tab-2":
        return constants.ACERCA_DE_BODY_METODOLOGIA
    elif active_tab == "tab-3":
        return constants.ESPACIO_CAF_BODY_METODOLOGIA
    else:
        return "Unknown tab selected"


# Run the app
if __name__ == '__main__':
    app.run_server(
        debug=False,
        host='0.0.0.0',
        port=8050
    )
