import streamlit as st
import pandas as pd
import joblib
import folium
from streamlit_folium import folium_static
import json
import boto3
from io import BytesIO, StringIO
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

try:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    if not AWS_ACCESS_KEY_ID:
        raise ValueError("Environment variable AWS_ACCESS_KEY_ID must be set")
    if not AWS_SECRET_ACCESS_KEY:
        raise ValueError("Environment variable AWS_SECRET_ACCESS_PWD must be set")

except ValueError as ve:
    print(f"Error: {ve}")
    
except Exception as e:
    print(f"An unexpected error occurred: {e}")


# Initialize S3 client
s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

bucket_name = 'airbnb-capstone-project'
def read_s3_file(file_key):
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    return obj['Body'].read()

# Use st.cache_data to cache data first time its downloaded
@st.cache_data
def load_model(allow_output_mutation=True):
    model_data = read_s3_file('models/model_h3.joblib')
    return joblib.load(BytesIO(model_data))

@st.cache_data
def load_hexagon_data():
    hexagon_data = read_s3_file('models/hexagon_data.csv')
    return pd.read_csv(StringIO(hexagon_data.decode('utf-8')))

@st.cache_data
def load_listings_data():
    listings_data = read_s3_file('models/listings_cleaned_h3.csv')
    return pd.read_csv(StringIO(listings_data.decode('utf-8')))

@st.cache_data
def load_geojson_data():
    geojson_data = read_s3_file('models/hexagon_data.geojson')
    return json.loads(geojson_data.decode('utf-8'))

# load model and data
pipeline = load_model()
hexagon_aggregated_data = load_hexagon_data()
listings_cleaned_h3 = load_listings_data()
geojson_data = load_geojson_data()


# Streamlit interface
st.title("Airbnb Lising Price Prediction")

# create market mapping
markets_dict = {
    'albany':'Albany',
    'chicago':'Chicago',
    'los-angeles':'Los Angeles',
    'new-york-city':'New York City',
    'san-francisco':'San Francisco',
    'seattle':'Seattle',
    'washington-dc':'Washington D.C.'
    }

# User input fields
market = st.selectbox("Market",  sorted(markets_dict.values()))
room_type = st.selectbox("Room Type", ['Entire home/apt', 'Hotel room','Private room','Shared room'])
beds = st.slider("Number of Beds", min_value=1, max_value=10, value=1)
accommodates = st.slider("Accommodates", min_value=1, max_value=16, value=1)
bathrooms = st.slider("Number of Bathrooms", min_value=1, max_value=6, value=1)

# Map the selected market back, e.g., New York City to new-york-city
reverse_markets_dict = {v: k for k, v in markets_dict.items()}
selected_market = reverse_markets_dict[market]

if 'price_recommendation' not in st.session_state:
    st.session_state['price_recommendation'] = None

if 'selected_market' not in st.session_state:
    st.session_state['selected_market'] = None

if 'map_data' not in st.session_state:
    st.session_state['map_data'] = None

# Predict button
if st.button("Get Listing Price Prediction"):
    # Filter hexagon_aggregated_data for the selected market
    market_data = hexagon_aggregated_data[hexagon_aggregated_data['market'] == selected_market]
    
    # Calculate overall median values for the selected market
    market_medians = market_data.median(numeric_only=True)

    # Create input df for prediction
    input_data = pd.DataFrame({
        'market': [selected_market],
        'room_type': [room_type],
        'accommodates': [accommodates],
        'bathrooms': [bathrooms],
        'beds': [beds],
        'accommodates_median': [market_medians['accommodates_median']],
        'bathrooms_median': [market_medians['bathrooms_median']],
        'beds_median': [market_medians['beds_median']],
        'price_median': [market_medians['price_median']]
    })

    # Make prediction using the loaded pipeline
    predicted_price = pipeline.predict(input_data)

    # store result in session state
    st.session_state['price_recommendation'] = predicted_price

price_recommendation = st.session_state['price_recommendation']

if st.session_state['price_recommendation'] is not None:
    st.markdown(f"Recommended Price: **${price_recommendation[0]:.2f}**")

st.write('')
st.subheader(f'Predicted listing prices for {market}')
st.write('Hexagons shown have a diameter of 1.4 km or 0.87 miles')

# Additional feature: Filter listings and generate predictions
if selected_market != st.session_state['selected_market']:
    # Market has changed so update the map
    st.session_state['selected_market'] = selected_market

    # Filter the listings based on user input
    filtered_listings = listings_cleaned_h3[listings_cleaned_h3['market'] == selected_market]

    # Prepare the filtered data for prediction
    filtered_input_data = filtered_listings.drop(columns=['price', 'latitude', 'longitude', 'h3_index'])

    # Generate predictions for the filtered data
    filtered_listings['predicted_price'] = pipeline.predict(filtered_input_data)

    # Store the predictions in session state
    st.session_state['map_data'] = filtered_listings

    # Create a Folium map
    map_center = [filtered_listings['latitude'].mean(), filtered_listings['longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=10, tiles='CartoDB positron')

    # Add Choropleth layer
    folium.Choropleth(
        geo_data=geojson_data,
        data=filtered_listings,
        columns=['h3_index', 'predicted_price'],
        key_on='feature.properties.h3_index',
        fill_color='OrRd',
        name='Hexagon',
        fill_opacity=0.5,
        line_opacity=0.2,
        legend_name='Predicted Listing Price'
    ).add_to(m)

    # Add tile layers for different viewing modes
    folium.TileLayer('cartodbdark_matter', overlay=True, name='Dark Mode', show=False).add_to(m)
    folium.TileLayer('openstreetmap', overlay=True, name='Open Street Map', show=False).add_to(m)
    folium.LayerControl(collapsed=True).add_to(m)

    # Use session_state to prevent the map from disappearing
    st.session_state.m = m


if st.session_state['map_data'] is not None:
    folium_static(st.session_state['m'], width=700, height=500)
