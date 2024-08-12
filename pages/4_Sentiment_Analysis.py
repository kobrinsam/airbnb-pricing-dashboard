import pandas as pd
import snowflake.connector
import os
from datetime import datetime
from dotenv import load_dotenv
import re
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
import streamlit as st


TEMP_USER=os.getenv('SNOWSQL_TEMP_USER')
TEMP_USER_PASSWORD=os.getenv('SNOWSQL_TEMP_PWD')
SNOWFLAKE_ACCOUNT=os.getenv('SNOWFLAKE_ACCOUNT')

# Cache Snowflake connection to avoid reconnecting on each run
@st.cache_resource
def connect_to_snowflake():
    try:
        conn = snowflake.connector.connect(
            user=TEMP_USER,
            password=TEMP_USER_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            warehouse='COMPUTE_WH',
            database='AIRBNB',
            schema='FEATURE_STORE'
        )
        print(f'Connected to Snowflake successfully')
        return conn
    except Exception as e:
        print(f'Failed to connect to Snowflake due to error code {e}')
        return None
    
conn = connect_to_snowflake()

# Cache NLTK resource downloads
@st.cache_data
def load_nltk_resources():
    libraries = ['stopwords', 'punkt', 'wordnet', 'omw-1.4', 'vader_lexicon']
    for lib in libraries:
        nltk.download(lib)

load_nltk_resources()


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

# Function to get data
def fetch_data(query):
    try:
        # Execute the query and fetch the data into a DataFrame
        return(pd.read_sql(query, conn))
    
    except Exception as e:
        print(f"Failed to execute query due to error: {e}")


# Clear the progress bar and status text when done
# progress_bar.empty()
# status_text.text("Download complete!")

stop_words = set(stopwords.words('english'))


def wordcloud(df):
    # Generate word cloud for cleaned comments
    text = ' '.join(df['clean_comments'])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    # Use Streamlit to display the figure
    plt.show()


def sentiment_distribution(df):
    df['sentiment'].value_counts().plot(kind='bar', figsize=(10, 5), color=['green', 'red', 'blue'])
    plt.xlabel('Sentiment')
    plt.ylabel('Frequency')
    plt.title('Distribution of Sentiment')
    plt.show()

def sentiment_histogram(df):
    # Plot histogram of sentiment scores
    plt.figure(figsize=(10, 5))
    plt.hist(df['sentiment_score'], bins=20, color='skyblue', edgecolor='black')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Frequency')
    plt.title('Distribution of Sentiment Scores')
    plt.show()

def trends_over_time(df):
    # Convert REVIEW_DATE to datetime
    df['review_date'] = pd.to_datetime(df['review_date'])

    # Group by date and sentiment to count occurrences
    sentiment_trend = df.groupby([df['review_date'].dt.date, 'sentiment']).size().unstack().fillna(0)

    # Plot the trends over time
    sentiment_trend.plot(kind='line', figsize=(15, 7))
    plt.xlabel('Date')
    plt.ylabel('Number of Reviews')
    plt.title('Sentiment Trends Over Time')
    plt.show()

def ngram_analysis(df, n=2):
    vectorizer = CountVectorizer(ngram_range=(n, n), stop_words='english')
    ngrams = vectorizer.fit_transform(df['clean_comments'])
    ngram_counts = ngrams.sum(axis=0).tolist()[0]
    ngram_features = vectorizer.get_feature_names_out()
    
    ngram_freq = dict(zip(ngram_features, ngram_counts))
    sorted_ngrams = sorted(ngram_freq.items(), key=lambda x: x[1], reverse=True)[:20]
    
    ngrams, counts = zip(*sorted_ngrams)
    
    plt.figure(figsize=(10, 5))
    plt.bar(ngrams, counts)
    plt.xlabel(f'{n}-grams')
    plt.ylabel('Frequency')
    plt.title(f'Top 20 Most Common {n}-grams')
    plt.xticks(rotation=45, fontsize=10, ha='right')  # Set fontsize for x-ticks
    plt.tight_layout()
    plt.show()

# Function to run all functions
def create_visualizations(city):
    # Enclose the city name in single quotes
    city_query = f"SELECT * FROM REVIEWS_SENTIMENT_SCORES SAMPLE (25) WHERE market = '{city}';" # randomly sample 25% of the data
    
    city_df = fetch_data(city_query)
    city_df.columns = [col.lower() for col in city_df.columns]
        
    # Generate and display the word cloud
    city_wordcloud = wordcloud(city_df)
    st.pyplot()  # Display the word cloud figure
    
    # Display sentiment histogram
    sentiment_hist = sentiment_histogram(city_df)
    st.pyplot(sentiment_hist)
    
    # Display sentiment distribution
    sentiment_dist = sentiment_distribution(city_df)
    st.pyplot(sentiment_dist)
    
    # Display trends over time
    trends_fig = trends_over_time(city_df)
    st.pyplot(trends_fig)
    
    # Display n-gram analysis for bigrams
    ngram_fig_2 = ngram_analysis(city_df, n=2)
    st.pyplot(ngram_fig_2)
    
    # Display n-gram analysis for trigrams
    ngram_fig_3 = ngram_analysis(city_df, n=3)
    st.pyplot(ngram_fig_3)

# Trigger download of data and generate visualizations
if st.button('Generate Visualizations'):
    # Show a progress bar and execute the function
    with st.spinner('Generating visualizations...'):
        create_visualizations(selected_market)