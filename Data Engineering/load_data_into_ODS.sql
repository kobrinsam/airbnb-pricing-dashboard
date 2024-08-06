-- copy listings from staging to ODS schema
COPY INTO listings
FROM @processed_listings_stage/
FILE_FORMAT = (FORMAT_NAME = 'my_parquet_format')
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

-- copy reviews from staging to ODS schema
COPY INTO reviews
FROM @processed_reviews_stage/
FILE_FORMAT = (FORMAT_NAME = 'my_parquet_format')
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

