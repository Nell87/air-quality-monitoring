# Running the data pipeline
from pathlib import Path
from extract import AqiAPI
from dbManager import DatabaseManager
import os
import requests
import psycopg2 
import pandas as pd

# Accessing the database/API configuration from environment variables
dbparam = {
    'user': os.getenv('SUPABASE_AIRQUALITY_DB_USER'),
    'password': os.getenv('SUPABASE_AIRQUALITY_DB_PASSWORD'),
    'host': os.getenv('SUPABASE_AIRQUALITY_DB_HOST'),
    'dbname': os.getenv('SUPABASE_AIRQUALITY_DBNAME'),
    'port': os.getenv('SUPABASE_AIRQUALITY_DB_PORT')
}

token = os.getenv('AQI_API_TOKEN')

# List of cities 
cities = ['Barcelona', 'Madrid', 'Cadiz']

# String conection
connection_string = f"dbname={dbparam['dbname']} user={dbparam['user']} password={dbparam['password']} host={dbparam['host']} port={dbparam['port']}"

def main():
  # Initialize your API and Database instance
  aqi_api = AqiAPI(token)
  dbmanager_instance = DatabaseManager(connection_string)
  conn = dbmanager_instance.create_connection()
  
  for city in cities:
    # Extract
    data = aqi_api.extract_data(city)
  
    # Insert in db
    dbmanager_instance.insert_data(conn,data)
  
  conn.close()
  
main()
