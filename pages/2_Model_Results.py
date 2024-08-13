import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import joblib
import boto3
from io import BytesIO, StringIO
import os
from dotenv import load_dotenv
import streamlit as st

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

def load_model():
    model_data = read_s3_file('models/regression_pipeline.joblib')
    return joblib.load(BytesIO(model_data))

@st.cache_data
def load_experiment_logs():
    json_data = read_s3_file('models/experiment_log.json')
    return json.loads(json_data)

# load experiment logs
experiment_logs = load_experiment_logs()

st.title('Model Results')

# Extract relevant information from log file
extracted_data = []

for log in experiment_logs:
    model_type = log['params']['model_type']
    test_mae = log['metrics']['test_mae']
    test_rmse = log['metrics']['test_rmse']
    extracted_data.append({
        'model_type': model_type,
        'test_mae': test_mae,
        'test_rmse': test_rmse
    })

df = pd.DataFrame(extracted_data)

# Sort by test_mae
df = df.drop_duplicates('model_type').sort_values('test_mae', ascending=False)
df = df.round(1)

def plot_model_performance():
    # Create the bar chart
    fig = plt.figure(figsize=(10, 8))
    # Create an array with the positions of each bar on the y axis
    y_pos = np.arange(len(df['model_type']))
    # Plot the bars, shifting each bar's position slightly
    plt.barh(y_pos + 0.2, df['test_mae'], 0.4, color='darkblue', label='Test MAE')
    plt.barh(y_pos - 0.2, df['test_rmse'], 0.4, color='lightblue', label='Test RMSE')

    # Add a title and axis titles
    plt.title('Airbnb List Price Prediction Model Performance', fontsize=20)
    plt.xlabel('Test Set Error (USD)')
    plt.ylabel('Model Type')

    # Replace the y ticks with the model type
    plt.yticks(y_pos, df['model_type'])

    # Add numbers to the ends of the bars
    for i in range(len(df['model_type'])):
        plt.text(df['test_mae'].iloc[i], y_pos[i] + 0.2, str(df['test_mae'].iloc[i]), va='center')
        plt.text(df['test_rmse'].iloc[i], y_pos[i] - 0.2, str(df['test_rmse'].iloc[i]), va='center')

    # Add a legend
    plt.legend()

    # Return the figure
    return fig
    
model = load_model()

def plot_feature_importance():

    # Get feature importances
    feature_importances =  model.named_steps['regressor'].feature_importances_
    #list of features in the model
    numerical_features = ['accommodates', 'bathrooms', 'beds', 'latitude', 'longitude']
    categorical_features = ["market", "room_type"] 
    # Get the one-hot encoded feature names for categorical features
    onehot_feature_names = model.named_steps['preprocessor'].transformers_[1][1].named_steps['onehot'].get_feature_names_out(categorical_features)

    # Combine numerical and categorical feature names
    all_feature_names = numerical_features + onehot_feature_names.tolist()

    # Create a dictionary of feature importances
    feature_importance_dict = dict(zip(all_feature_names, feature_importances))
    feature_importance_df = pd.DataFrame(feature_importance_dict.items(), columns=['Feature', 'Importance']).sort_values('Importance', ascending=False)

    # Sort the DataFrame by importance
    feature_importance_df = feature_importance_df.sort_values('Importance')

    # Create the bar chart
    fig = plt.figure(figsize=(10, 6))
    plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'], color='darkblue')

    # Add a title and axis titles
    plt.title('Feature Importance Score (Random Forests)', fontsize=20)
    plt.xlabel('Importance')
    plt.ylabel('Feature Name')

    # Return the figure
    return fig

st.subheader('Original Model')
st.write('### Model Performance')
fig1 = plot_model_performance()
st.pyplot(fig1)

st.write('### Feature Performance')
st.image("../images/feature_importance.png", use_column_width=True)

st.subheader('H3 Model')
st.write('### Correlation Matrix')
st.image("../images/h3_model_correlation_matrix.png", use_column_width=True)

st.write('### Distribution of errors')
st.image("../images/h3_model_errors.png", use_column_width=True)