# Data Analysis
import pandas as pd
import numpy as np

# Plotly
import plotly.express as px

# Dash
from dash import Dash, dcc, html, Input, Output, ctx

# Bootstrap
import dash_bootstrap_components as dbc

# Local
import constants

# Credentials
from conf.credentials import MAPBOX_TOKEN

dataset = pd.read_csv("data/test_bogota_cuenca_data.csv")

dataset_neighborhoods = pd.read_csv(
    "data/test_bogota_cuenca_neighborhoods_data.csv")


def get_selector_graph(city, accesibility_means):

    fig = px.scatter(
        dataset_neighborhoods[dataset_neighborhoods.city == city],
        x=constants.ACCESIBILITY_MEANS[accesibility_means],
        y="population",
        size="population",
        color=constants.ACCESIBILITY_MEANS[accesibility_means],
        hover_name="neighborhood",
        log_x=False,
        size_max=20,
        height=250,
    )

    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_xaxes(visible=False, showticklabels=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(showlegend=False)
    fig.update_layout(plot_bgcolor="#343332")
    fig.update_traces(marker_sizemin=3, selector=dict(type='scatter'))

    fig.update_coloraxes(colorbar_orientation='h')
    fig.update_coloraxes(colorbar_thickness=10)
    fig.update_coloraxes(colorbar_title=dict(text=''))
    fig.update_coloraxes(colorbar_y=0.0)
    fig.update_coloraxes(colorbar_x=0.5)
    fig.update_coloraxes(colorbar_len=0.3)
    fig.update_coloraxes(colorbar_tickfont=dict(color="#f4f4f4"))

    return fig


def get_centered_map(city, accesibility_means, neighborhood):
    
    if neighborhood is None:
        lat = constants.CENTER_CITY_COORDINATES[city]['center_lat']
        lon = constants.CENTER_CITY_COORDINATES[city]['center_lon']
        zoom = 10
    else:
        lat = dataset_neighborhoods[dataset_neighborhoods.neighborhood==neighborhood].latitude.values[0]
        lon = dataset_neighborhoods[dataset_neighborhoods.neighborhood==neighborhood].longitude.values[0]
        zoom = 12

    fig = px.density_mapbox(
        dataset,
        lat="latitude",
        lon="longitude",
        z=constants.ACCESIBILITY_MEANS[accesibility_means],
        radius=10,
        hover_name="city",
        hover_data=["city", "accessibility_foot"],
        center=dict(lat=lat, lon=lon),
        zoom=zoom,
        opacity=1,
        mapbox_style="carto-darkmatter",
        # mapbox_style="open-street-map",

    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_coloraxes(colorbar_orientation='v')
    fig.update_coloraxes(colorbar_thickness=10)
    fig.update_coloraxes(colorbar_title=dict(text=''))
    fig.update_coloraxes(colorbar_y=0.2)
    fig.update_coloraxes(colorbar_x=0.92)
    fig.update_coloraxes(colorbar_len=0.3)
    fig.update_coloraxes(colorbar_tickfont=dict(color="#f4f4f4"))
    token = MAPBOX_TOKEN
    fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
    return fig


fig = get_centered_map(list(constants.CENTER_CITY_COORDINATES.keys())[
                       0], list(constants.ACCESIBILITY_MEANS.keys())[0],
                       None)

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
                            html.H5("Accesibilidad",
                                    className="card-title"),
                            html.P(
                                "Some quick example text to build on the card title and make "
                                "up the bulk of the card's content.",
                                className="card-text",
                            ),
                            html.H6('Ciudad'),
                            dcc.Dropdown(
                                options=list(constants.CENTER_CITY_COORDINATES.keys()),
                                value=list(constants.CENTER_CITY_COORDINATES.keys())[0],
                                id=constants.CITY_SELECTOR,
                                clearable=False
                            ),
                            html.H6('Medio de acceso'),
                            dcc.Dropdown(
                                options=list(constants.ACCESIBILITY_MEANS.keys()),
                                value=list(constants.ACCESIBILITY_MEANS.keys())[0],
                                id=constants.ACCESIBILITY_SELECTOR,
                                clearable=False
                            ),
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
                                        figure=fig,
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
                        [html.P("Seleccione un punto de la gráfica para ver los datos de una localidad.", className='graph-selector-text'),
                         dcc.Graph(
                            id=constants.SCATTER_ID,
                            figure=get_selector_graph(
                                list(constants.CENTER_CITY_COORDINATES.keys())[0],
                                list(constants.ACCESIBILITY_MEANS.keys())[0]
                            ),
                            config={
                                'displayModeBar': False
                            },
                            style={"height": "100%",
                                   "width": "100%"},
                        )],
                    ),
                ],
                className='map-container'
            ),
        ]
    ),
    ]
)


@ app.callback(
    [
        Output(component_id=constants.MAP_ID, component_property='figure'),
        Output(component_id=constants.SCATTER_ID, component_property='figure')
    ],
    [
        Input(component_id=constants.CITY_SELECTOR, component_property='value'),
        Input(component_id=constants.ACCESIBILITY_SELECTOR,
              component_property='value'),
        Input(component_id=constants.SCATTER_ID,
              component_property='hoverData'),
    ]
)
def update_output_div(city, accesibility_means, clicked_neighborhoods):
    triggered_input = ctx.triggered_id
    if (triggered_input == constants.SCATTER_ID or triggered_input == constants.ACCESIBILITY_SELECTOR):
        neighborhood =  clicked_neighborhoods['points'][0]['hovertext']
    else:
        neighborhood = None
    return get_centered_map(city, accesibility_means, neighborhood), get_selector_graph(city, accesibility_means)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

