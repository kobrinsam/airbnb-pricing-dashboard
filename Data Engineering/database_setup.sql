-- SQL script to create Snowflake database and schemas

-- Create a new database called 'airbnb'
CREATE DATABASE IF NOT EXISTS airbnb;

-- Switch to the 'airbnb' database
USE DATABASE airbnb;

-- Create a schema called 'ods' within the 'airbnb' database
CREATE SCHEMA IF NOT EXISTS ods;

-- Create a schema called 'feature_store' within the 'airbnb' database
CREATE SCHEMA IF NOT EXISTS feature_store;

-- Show all schemas in the 'airbnb' database
SHOW SCHEMAS IN DATABASE airbnb;