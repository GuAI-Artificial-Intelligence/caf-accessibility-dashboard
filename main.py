import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")

fig = px.scatter_mapbox(
    us_cities, 
    lat="lat", 
    lon="lon", 
    hover_name="City", 
    hover_data=["State", "Population"],
    color_discrete_sequence=["fuchsia"], 
    center=dict(lat=4.63, lon=-74.11),
    zoom=10.5, 
)

fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(mapbox_style="carto-darkmatter")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


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
            }
        )
    ]
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)