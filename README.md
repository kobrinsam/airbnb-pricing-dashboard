# Airbnb Pricing Dashboard

This project is a web-based dashboard that helps Airbnb hosts determine the best possible price for their listings. It uses a random forests machine learning model to predict listing prices based on various factors such as location, room type and number of guests.

## Features

- Interactive dashboard with user inputs for AirBnB listing details
- Price prediction using a Random Forest machine learning model
- Map visualization showing predicted prices across neigborhoods of selected markets
- Documentation of selected exploratory data analysis and model performance

## Installation

1. Clone this repository.
2. Install the required dependencies with `pip install -r requirements.txt`.
3. Set up AWS and Snowflake credentials (see section below for details).
4. Run the dashboard locally with `streamlit run Home.py`. The Streamlit app is hosted online [here](https://airbnb-pricing-dashboard-m2gvwrulwcmashpo95zmal.streamlit.app/).

In addition to the dashboard above, we performed exploratory data analysis, data cleaning, and model training as preparation for production. Data engineering scripts can be found in the data_engineering folder. Model training occurred in train.ipynb and H3_Model_Development.ipynb. Our exploratory data analysis can be reproduced from the Exploratory_Data_Analysis folder. Model run results are logged in experiment_log.json.

### AWS and Snowflake Setup

#### Setting Up Your Credentials

The `.env` file serves as a centralized location to store sensitive information such as API keys, access tokens, database connection strings, etc. Create a blank file and save it as `.env` with the following keys:

```env
AWS_ACCESS_KEY_ID="your_access_key"
AWS_SECRET_ACCESS_KEY="your_secret_key"
SNOWFLAKE_USER="your_username"
SNOWFLAKE_PWD="your_password"
SNOWFLAKE_ACCOUNT="snowflake_account"
```

#### AWS

To follow along, you will need an AWS and Snowflake account. Start by creating a bucket and creating the following folder structure:
```
raw/
processed/
models/
```
The Python scripts will download, process, and store the data within the necessary folders. After setting up your environment variables, a connection to S3 can be established using:
```python
import boto3

s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)
```

#### Snowflake

Sign up for a free trial with [Snowflake](https://www.snowflake.com/en/) and store your credentials in the .env file. Setup two schemas, one called ODS and the other FEATURE_STORE. These two schemas will be used to store the data after initial processing is completed and after feature engineering is completed.  You will need to create an external stage which links your S3 bucket to your Snowflake account. Instructions can be found [here](https://docs.snowflake.com/en/user-guide/data-load-s3-create-stage). Once your external stage is setup, Snowflake will load data from S3 into the ODS schema.

## Usage

1. Open the dashboard in your web browser.
2. Enter the details of your Airbnb listing.
3. The price prediction page of the dashboard will display the predicted list price for your AirBnb listing.

## Data Access Statement
The data used in this project was accessed from Inside AirBnB on July 7, 2024. The data can be acessed here http://insideairbnb.com/get-the-data. The dataset includes listing and review information collected during June and July of 2024 for the following target markets: Albany, NY; Los Angeles, CA; San Francisco, CA; New York, NY; Chicago, IL; Seattle, WA; and Washington, DC.

Please ensure compliance with Inside AirBnB's license for usage and distribution before accessing or using the data. For more details, refer to their data policies at Inside AirBnB Data Policies and visit their main website at Inside AirBnB.

## License

This project is licensed under the MIT LICENSE - see the [LICENSE](LICENSE) file for details.

