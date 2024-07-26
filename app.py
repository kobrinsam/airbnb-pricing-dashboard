import pandas as pd
import joblib
from shiny import App, render, ui, reactive
from ipyleaflet import Map, Marker, basemaps
from shinywidgets import output_widget, render_widget
import ipywidgets as widgets

# Load the pre-trained model from pickle file
model = joblib.load('regression_pipeline.joblib')

# Centroids of the cities to intailize the map
city_centroids = {
    'albany': (42.6526, -73.7562),
    'chicago': (41.8781, -87.6298),
    'los-angeles': (34.0522, -118.2437),
    'new-york-city': (40.7128, -74.0060),
    'san-francisco': (37.7749, -122.4194),
    'seattle': (47.6062, -122.3321),
    'washington-dc': (38.9072, -77.0369)
}

# Define the UI layout
app_ui = ui.page_fluid(
    ui.panel_title("AirBnB Price Prediction Dashboard"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select("market", "Market", {
                "albany": "Albany", 
                "chicago": "Chicago", 
                "los-angeles": "Los Angeles", 
                "new-york-city": "New York", 
                "san-francisco": "San Francisco", 
                "seattle": "Seattle", 
                "washington-dc": "Washington"
            }),
            ui.input_select("room_type", "Room Type", {
                "Entire home/apt": "Entire home/apt", 
                "Private room": "Private room", 
                "Shared room": "Shared room"
            }),
            ui.input_slider("accommodates", "Accommodates", min=1, max=10, value=2),
            ui.input_slider("bathrooms", "Bathrooms", min=1, max=5, value=1),
            ui.input_slider("beds", "Beds", min=1, max=10, value=1)
        ),
        ui.panel_main(
            ui.output_text_verbatim("prediction"),
            output_widget("map")
        )
    )
)

# Define the server logic
def server(input, output, session):
    lat_lon = reactive.Value((0, 0))  # Store latitude and longitude
    marker = Marker(location=(0, 0))
    map_widget = Map(center=(37.7749, -122.4194), zoom=12, basemap=basemaps.OpenStreetMap.Mapnik)
    map_widget.add_layer(marker)
    @reactive.Calc
    def user_input():
        data = {
            'market': [input.market()],
            'room_type': [input.room_type()],
            'accommodates': [input.accommodates()],
            'bathrooms': [input.bathrooms()],
            'beds': [input.beds()],
            'latitude': [lat_lon.get()[0]],
            'longitude': [lat_lon.get()[1]]
        }
        return pd.DataFrame(data)

    @output
    @render.text
    def prediction():
        df = user_input()
        pred = model.predict(df)
        return f"Predicted AirBnB Price: ${pred[0]:.2f}"
    #  Update the marker location based on map click
    def on_map_click(event, **kwargs):
        lat = kwargs.get('coordinates')[0]
        lon = kwargs.get('coordinates')[1]
        lat_lon.set((lat, lon))
        marker.location = (lat, lon)
    
    map_widget.on_interaction(on_map_click)
    # Render the map widget
    @output
    @render_widget
    def map():
        market = input.market()
        lat, lon = city_centroids.get(market, (37.7749, -122.4194))
        map_widget.center = (lat, lon)
        map_widget.zoom = 12
        return map_widget

# Create the Shiny app
app = App(app_ui, server)

# Run the app (if running this script directly)
if __name__ == "__main__":
    app.run()
