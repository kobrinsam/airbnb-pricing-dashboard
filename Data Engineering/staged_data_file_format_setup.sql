-- create a csv file format
CREATE OR REPLACE FILE FORMAT my_csv_format
        TYPE = 'CSV'
        FIELD_OPTIONALLY_ENCLOSED_BY = '"'
        SKIP_HEADER = 1
        COMPRESSION = 'GZIP';

-- create a parquet file format
CREATE FILE FORMAT my_parquet_format
  TYPE = parquet;