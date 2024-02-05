# Running the data pipeline
from pathlib import Path
from extract import AqiAPI
from dbManager import DatabaseManager
import os
import requests
import psycopg2 
import pandas as pd
from config import dbparam, token, cities, connection_string

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
