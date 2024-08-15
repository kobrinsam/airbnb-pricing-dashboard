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
3. Run the dashboard locally with `streamlit run Home.py`. App is published at https://airbnb-pricing-dashboard-m2gvwrulwcmashpo95zmal.streamlit.app/

In addition to the dashboard above, we performed exploratory data analysis, data cleaning, and model training as preparation for production. Data engineering scripts can be found in the data_engineering folder. Model training occurred in train.ipynb and H3_Model_Development.ipynb. Our exploratory data analysis can be reproduced from the Exploratory_Data_Analysis folder. Model run results are logged in experiment_log.json.

## Usage

1. Open the dashboard in your web browser.
2. Enter the details of your Airbnb listing.
3. The dashboard will display the predicted list price for your AirBnb listing.

## Data Access Statement
The data used in this project was accessed from Inside AirBnB on July 7, 2024. The data can be acessed here http://insideairbnb.com/get-the-data. The dataset includes listing and review information collected during June and July of 2024 for the following target markets: Albany, NY; Los Angeles, CA; San Francisco, CA; New York, NY; Chicago, IL; Seattle, WA; and Washington, DC.

Please ensure compliance with Inside AirBnB's license for usage and distribution before accessing or using the data. For more details, refer to their data policies at Inside AirBnB Data Policies and visit their main website at Inside AirBnB.

## License

This project is licensed under the MIT LICENSE - see the [LICENSE](LICENSE) file for details.

## Credits

This project was developed with the assistance of [GitHub Copilot](https://github.com/features/copilot), which was used to expedite the code development process. GitHub Copilot provided code suggestions and code completions, helping to expedite the development process.
