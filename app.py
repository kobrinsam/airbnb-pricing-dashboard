import pandas as pd
import numpy as np
import joblib
from shiny import App, render, ui, reactive

# Load the pre-trained model from a pickle file
model = joblib.load('regression_pipeline.joblib')
#- albany
#- chicago
#- los-angeles
#- new-york-city
#- san-francisco
#- seattle
#- washington-dc
# Define the UI layout
app_ui = ui.page_fluid(
    ui.panel_title("AirBnb Price Prediction Dashboard"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select("market", "Market", {"albany": "Albany", "chicago": "Chicago", "los-angeles": "Los Angeles", "new-york-city": "New York", "san-francisco": "San Francisco", "seattle": "Seattle", "washington-dc": "Washington"}), # note need to change selctions to mactch the dataset
            ui.input_select("room_type", "Room Type", {"Entire home/apt": "Entire home/apt", "Private room": "Private room", "Shared room": "Shared room"}),
            ui.input_select("host_identity_verified", "Host Identity Verified", {"True": "True", "False": "False"}),
            ui.input_slider("accommodates", "Accommodates", min=1, max=10, value=1),
            ui.input_slider("bathrooms", "Bathrooms", min=1, max=5, value=1),
            ui.input_slider("beds", "Beds", min=1, max=10, value=1)
        ),
        ui.panel_main(
            ui.output_text_verbatim("prediction")
        )
    )
)

# Define the server logic
def server(input, output, session):

    @reactive.Calc
    def user_input():
        data = {
            'market': [input.market()],
            'room_type': [input.room_type()],
            'host_identity_verified': [input.host_identity_verified()],
            'accommodates': [input.accommodates()],
            'bathrooms': [input.bathrooms()],
            'beds': [input.beds()]
        }
        return pd.DataFrame(data)

    @output
    @render.text
    def prediction():
        df = user_input()
        pred = model.predict(df)
        return f"Predicted Price: ${pred[0]:.2f}"

# Create the Shiny app
app = App(app_ui, server)

# Run the app (if running this script directly)
if __name__ == "__main__":
    app.run()
