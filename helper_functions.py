## this file contains helper funtions that are used in mutliple notebooks
import pandas as pd
import snowflake.connector
import os
from datetime import datetime
from dotenv import load_dotenv
from snowflake.connector.pandas_tools import write_pandas
import logging

# Set up logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

def connect_to_snowflake(schema_name=None):
    # Load environment variables from a .env file
    load_dotenv()

    SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
    SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PWD')
    SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
    
    if not SNOWFLAKE_USER:
        logger.error("Environment variable SNOWFLAKE_USER must be set")
        return None
    if not SNOWFLAKE_PASSWORD:
        logger.error("Environment variable SNOWFLAKE_PWD must be set")
        return None

    try:
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            warehouse='COMPUTE_WH',
            database='AIRBNB',
            schema=schema_name
        )

        print(f'Successfully connected to Snowflake schema {schema_name}')
        return conn

    except snowflake.connector.errors.Error as e:
        logger.error(f'Failed to connect to Snowflake due to error: {e}')
        return None


def get_data(sql_query, conn, date_columns=None):
    """
    Executes a SQL query and returns the result as a pandas DataFrame.

    Args:
        sql_query (str): SQL query to execute.
        conn (snowflake.connector): Snowflake connection object.
        date_columns (list, optional): List of columns to parse as dates

    Returns:
        df_result: Resulting DataFrame from the SQL query.
    """
    try:
        cursor = conn.cursor()
        
        cursor.execute(sql_query)

        # load data into dataframe
        df_result = cursor.fetch_pandas_all()

        # Convert column names to lowercase
        df_result.columns = map(str.lower, df_result.columns)

        # Parse specified date columns
        if date_columns:
            for col in date_columns:
                df_result[col] = pd.to_datetime(df_result[col], errors='coerce')

    finally:
        if cursor is not None:
            cursor.close()

    return df_result


def write_to_snowflake(df_name, conn, schema_name, table_name, overwrite_table=False):
    """
    Writes data from dataframe to Snowflake.

    Args:
        df_name (str): Name of the DataFrame to write to Snowflake.
        conn (snowflake.connector): Snowflake connection object.
        snowflake_schema_name (str): Name of the schema to write to in Snowflake
        snowflake_table_name (str): Name of the table to write to in Snowflake.
    Returns:
        Writes data to Snowflake.
    """
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M%S')

    schema_name = str.upper(schema_name)
    table_name = str.upper(table_name)

    try:
        success, num_chunks, num_rows, output = write_pandas(
            conn=conn,
            df=df_name,
            schema=schema_name, # schema needs to be capitalized
            table_name=table_name,
            auto_create_table=True,
            overwrite=overwrite_table
        )

        if overwrite_table:
            print(f'Table {table_name} created in schema {schema_name} at {current_time}')
        else:
            print(f'Data appended to table {table_name} in schema {schema_name} at {current_time}')

    except Exception as e:
        logger.error(f'Failed to create table and load data to Snowflake due to error code {e}')