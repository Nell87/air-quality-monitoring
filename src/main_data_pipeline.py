# Basic libraries
import os
import sys 
import pandas as pd
import psycopg2 
import requests
from pathlib import Path

# Paths 
sys.path.append(os.path.abspath('./data_pipeline/'))

# Own libraries
from extract import AqiAPI
from dbManager import DatabaseManager
from config import dbparam, token, cities, connection_string

# Running the data pipeline
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
