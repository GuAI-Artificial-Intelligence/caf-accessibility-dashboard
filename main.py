# Python 
import random

# Data Analysis
import pandas as pd

# Plotly
import plotly.express as px

# Dash
from dash import Dash, dcc, html, Input, Output

# Bootstrap
import dash_bootstrap_components as dbc

# Local
from constants import CENTER_CITY_COORDINATES

# Credentials
from conf.credentials import MAPBOX_TOKEN

dataset = pd.read_csv("data/test_bogota_cuenca_data.csv")
df = px.data.gapminder()
df['x'] = [random.randint(0, 100) for i in range(df.shape[0])]
df['y'] = [random.uniform(1.5, 1.9) for i in range(df.shape[0])]

def get_selector_graph():
    fig = px.scatter(
        df.query("year==2007"),
        x="x",
        y="y",
        size="x",
        color="x",
        hover_name="country",
        log_x=True,
        size_max=50,
        height=250,
    )
    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_xaxes(visible=False, showticklabels=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(showlegend=False)
    fig.update_layout(plot_bgcolor="#343332")
    fig.update_traces(marker_sizemin=5, selector=dict(type='scatter'))

    fig.update_coloraxes(colorbar_orientation='h')
    fig.update_coloraxes(colorbar_thickness=10)
    fig.update_coloraxes(colorbar_title=dict(text=''))
    fig.update_coloraxes(colorbar_y=0.0)
    fig.update_coloraxes(colorbar_x=0.5)
    fig.update_coloraxes(colorbar_len=0.3)
    fig.update_coloraxes(colorbar_tickfont=dict(color="#f4f4f4"))

    return fig


def centered_map(city):
    lat = CENTER_CITY_COORDINATES[city]['center_lat']
    lon = CENTER_CITY_COORDINATES[city]['center_lon']
    fig = px.density_mapbox(
        dataset,
        lat="latitude",
        lon="longitude",
        z='Accesibilidad',
        radius=10,
        hover_name="city",
        hover_data=["city", "Accesibilidad"],
        # color_discrete_sequence=["fuchsia"],
        center=dict(lat=lat, lon=lon),
        zoom=10,
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


fig = centered_map('Bogotá')

# Create a Dash app
app = Dash(
    external_stylesheets=['assets/base.css', dbc.themes.BOOTSTRAP]
)

app.layout = html.Div(
    dbc.Row(
        children=[
            dbc.Col(
                width=4,
                className='panel-control-container',
                children=[
                    # dbc.Card(
                    html.Div(
                        children=[
                            html.H5("Accesibilidad",
                                    className="card-title"),
                            html.P(
                                "Some quick example text to build on the card title and make "
                                "up the bulk of the card's content.",
                                className="card-text",
                            ),
                            dcc.Dropdown(
                                options=['Bogotá', 'Cuenca'],
                                value='Bogotá',
                                id='my-city-selector',
                                clearable=False
                            ),
                            # dbc.CardLink("Card link", href="#"),
                            # dbc.CardLink("External link",
                            #              href="https://google.com"),
                        ],
                        className='panel-control-content'
                    ),
                    # ),

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
                                        id="my-map"
                                    )
                                ],
                                className='map-content'
                            ),
                        ],
                    ),
                    dbc.Row(
                        [html.P("Seleccione un punto de la gráfica para ver los datos de una localidad.", className='graph-selector-text'),
                        dcc.Graph(
                            figure=get_selector_graph(),
                            config={
                                'displayModeBar': False
                            },
                            style={"height": "100%",
                                   "width": "100%"},
                        )],
                        # children=[
                        # px.scatter(
                        #     df.query("year==2007"),
                        #     x="gdpPercap",
                        #     y="lifeExp",
                        #     size="pop",
                        #     color="continent",
                        #     hover_name="country",
                        #     log_x=True,
                        #     size_max=60
                        # )
                        # ]df = px.data.gapminder()
                    ),
                ],

                className='map-container'
            ),
        ]
    )

)
# app.layout = html.Div(
#     style={"height": "100vh", "width": "100vw"},
#     children=[
#         dcc.Graph(
#             figure=fig,
#             style={"height": "100vh", "width": "100vw"},
#             config={
#                 'displayModeBar': False
#             },
#             id="my-map"
#         ),
#         html.Div(

#             html.Div(
#                 children=[
#                     html.H3('Ciudades'),
#                     dcc.RadioItems(
#                         options=['Bogotá', 'Cuenca'],
#                         value='Bogotá',
#                         id='my-city-selector'
#                     ),
#                 ],
#                 className='control-panel-content'
#             ),
#             className='control-panel',
#         )
#     ]
# )


@ app.callback(
    Output(component_id='my-map', component_property='figure'),
    Input(component_id='my-city-selector', component_property='value')
)
def update_output_div(input_value):
    return centered_map(input_value)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
