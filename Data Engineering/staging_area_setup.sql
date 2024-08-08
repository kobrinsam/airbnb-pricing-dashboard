-- SQL script to setup staging areas in Snowflake

CREATE STAGE PROCESSED_LISTINGS_STAGE
URL='s3://airbnb-capstone-project/processed/listings/'
CREDENTIALS=(AWS_KEY_ID='your_aws_key_id' AWS_SECRET_KEY='your_aws_secret_key')
FILE_FORMAT=(TYPE='PARQUET');


CREATE STAGE PROCESSED_REVIEWS_STAGE
URL='s3://airbnb-capstone-project/processed/reviews/'
CREDENTIALS=(AWS_KEY_ID='your_aws_key_id' AWS_SECRET_KEY='your_aws_secret_key')
FILE_FORMAT=(TYPE='PARQUET');