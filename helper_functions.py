## this file contains helper funtions that are used in mutliple notebooks
import pandas as pd
import snowflake.connector
import os
from datetime import datetime
from dotenv import load_dotenv
from snowflake.connector.pandas_tools import write_pandas

def get_data(sql_query, conn, date_columns=None):
    """
    Executes a SQL query and returns the result as a pandas DataFrame.

    Args:
        sql_query (str): SQL query to execute.

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


def write_to_snowflake(df_name, conn, snowflake_schema_name, snowflake_table_name):
    """
    Executes a SQL query to write data to Snowflake.

    Args:
        df_name (str): Name of the DataFrame to write to Snowflake.
        snowflake_schema_name (str): Name of the schema to write to in Snowflake
        snowflake_table_name (str): Name of the table to write to in Snowflake.
        conn (snowflake.connector): Snowflake connection object.
    Returns:
        None. Writes data to Snowflake.
    """
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M%S')
    try:
        success, num_chunks, num_rows, output = write_pandas(
            conn=conn,
            df=df_name,
            schema= str.upper(snowflake_schema_name), # schema needs to be capitalized
            table_name=snowflake_table_name,
            auto_create_table=True,
            overwrite=True
        )

        print(f'Created table and data loaded to Snowflake at {current_time}')

    except Exception as e:
        print(f'Failed to create table and load data to Snowflake due to error code {e}')
    return None