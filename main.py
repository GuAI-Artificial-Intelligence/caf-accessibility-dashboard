import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

from constants import CENTER_CITY_COORDINATES

bogota_dataset = pd.read_csv("data/test_bogota_cuenca_data.csv")


def centered_map(city):
    lat = CENTER_CITY_COORDINATES[city]['center_lat']
    lon = CENTER_CITY_COORDINATES[city]['center_lon']
    fig = px.density_mapbox(
        bogota_dataset, 
        lat="latitude", 
        lon="longitude", 
        z='population',
        radius=10,
        hover_name="city", 
        hover_data=["city", "population"],
        # color_discrete_sequence=["fuchsia"], 
        center=dict(lat=lat, lon=lon),
        zoom=10.5, 
        opacity=1,
        mapbox_style="open-street-map",
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

fig = centered_map('Bogotá')

# Create a Dash app
app = Dash(
    external_stylesheets=['assets/base.css']
)
app.layout = html.Div(
    style={"height": "100vh", "width": "100vw"},
    children=[
        dcc.Graph(
            figure=fig,
            style={"height": "100vh", "width": "100vw"},
            config={
                'displayModeBar': False
            },
            id="my-map"
        ),
        dcc.RadioItems(
            className='control-panel',
            options=['Bogotá', 'Cuenca'],
            value='Bogotá',
            id='my-city-selector'
        )
    ]
)

@app.callback(
    Output(component_id='my-map', component_property='figure'),
    Input(component_id='my-city-selector', component_property='value')
)
def update_output_div(input_value):
    return centered_map(input_value)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)