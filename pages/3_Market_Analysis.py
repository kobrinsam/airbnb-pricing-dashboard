import pandas as pd
import folium
import h3
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_folium import folium_static
import json
import boto3
from io import BytesIO, StringIO
import os
from dotenv import load_dotenv

st.title('Market Analysis')

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

# Initialize S3 client
s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

bucket_name = 'airbnb-capstone-project'
def read_s3_file(file_key):
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    return obj['Body'].read()

@st.cache_data
def load_listings_data():
    listings_data = read_s3_file('models/listings_cleaned_h3.csv')
    return pd.read_csv(StringIO(listings_data.decode('utf-8')))

@st.cache_data
def load_geojson_data():
    geojson_data = read_s3_file('models/hexagon_data.geojson')
    return json.loads(geojson_data.decode('utf-8'))

listings_cleaned_h3 = load_listings_data()
geojson_data = load_geojson_data()

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

# Map the selected market back, e.g., New York City to new-york-city
reverse_markets_dict = {v: k for k, v in markets_dict.items()}
selected_market = reverse_markets_dict[market]

if 'selected_market' not in st.session_state:
    st.session_state['selected_market'] = None

if 'map_data' not in st.session_state:
    st.session_state['map_data'] = None

st.subheader(f'Actual median listing prices for {market}')
st.write('Hexagons shown have a diameter of 1.4 km or 0.87 miles')
st.write('Summary Statistics')

# Additional feature: Filter listings and generate predictions
if selected_market != st.session_state['selected_market']:
    # Market has changed so update the map
    st.session_state['selected_market'] = selected_market

    # Filter the listings based on user input
    filtered_listings = listings_cleaned_h3[listings_cleaned_h3['market'] == selected_market]

    min_price = int(filtered_listings['price'].min())
    max_price = int(filtered_listings['price'].max())
    median_price = int(filtered_listings['price'].median())
    unique_listings = len(filtered_listings)

    st.markdown(f'- Number of listings: **{unique_listings}**')
    st.markdown(f'- Min price: **${min_price}**')
    st.markdown(f'- Median price: **${median_price}**')
    st.markdown(f'- Max price: **${max_price}**')

    # Store the predictions in session state
    st.session_state['map_data'] = filtered_listings

    # Create a Folium map
    map_center = [filtered_listings['latitude'].mean(), filtered_listings['longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=10, tiles='CartoDB positron')

    # Add Choropleth layer
    folium.Choropleth(
        geo_data=geojson_data,
        data=filtered_listings,
        columns=['h3_index', 'price_median'],
        key_on='feature.properties.h3_index',
        fill_color='OrRd',
        name='Hexagon',
        fill_opacity=0.5,
        line_opacity=0.2,
        legend_name='Median Price'
    ).add_to(m)

    # Add tile layers for different viewing modes
    folium.TileLayer('cartodbdark_matter', overlay=True, name='Dark Mode', show=False).add_to(m)
    folium.TileLayer('openstreetmap', overlay=True, name='Open Street Map', show=False).add_to(m)
    folium.LayerControl(collapsed=True).add_to(m)

    # Use session_state to prevent the map from disappearing
    st.session_state.m = m


if st.session_state['map_data'] is not None:
    folium_static(st.session_state['m'], width=700, height=500)


st.divider()

st.write("This histogram shows the range of Airbnb prices across markets to help you see how your property’s price compares to others. Use this to check if your pricing is competitive and consider adjustments to align with market trends.")

def plot_histogram():
    # Plot the histogram
    fig = plt.figure(figsize=(10, 6))

    # Drop NaN values and create the histogram
    plt.hist(listings_cleaned_h3['price'].dropna(), bins=30, edgecolor='black')

    # Add titles and labels
    plt.title('Distribution of Airbnb Prices for All Markets')
    plt.xlabel('Price')
    plt.ylabel('Frequency')

    # Display grid for better readability
    plt.grid(True)

    # Show the plot
    return fig

st.write("The visualizations display Airbnb prices across markets with outliers removed to give you a clearer view of typical pricing. Outliers are identified and excluded based on the Interquartile Range (IQR), which is calculated using the 25th percentile (Q1) and the 75th percentile (Q3) of the price data. This method helps to remove extreme values that could skew the results and allow you to focus on the most relevant price ranges.")
def plot_boxplot():
    # Create a Seaborn boxplot for rental prices
    fig = plt.figure(figsize=(12, 6))
    plt.title('Boxplot of Airbnb Prices for Each Market')
    sns.boxplot(data=listings_cleaned_h3, x='market', y='price')

    return fig


fig1 = plot_histogram()
st.pyplot(fig1)

fig2 = plot_boxplot()
st.pyplot(fig2)