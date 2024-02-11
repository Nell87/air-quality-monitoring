# Basic libraries
import requests
import os
import configparser
import psycopg2 
import pandas as pd
import datetime

class DatabaseManager:
  """ Data extraction from the aqicn API 
  https://aqicn.org/api/
  """
  def __init__(self, connection_string):
        self.connection_string = connection_string
  
  def create_connection(self):
      """Create a connection to PostgreSQL database."""
      conn = None
      try:
          conn = psycopg2.connect(self.connection_string)
          conn.autocommit = True
          print("Connected to the database")
          return conn
        
      except psycopg2.Error as e:
          print(e, 'Error: Could not make connection to the Postgres database')
          return None
          
  def get_airquality_info(self,conn, columns=None, last_days=None):
      
      # Default columns to get if none are specified
      if columns is None:
          columns = ['city', 'time', 'aqi', 'inserted_timestamp']
            
      # Ensure columns are valid 
      valid_columns = {'city', 'time', 'aqi', 'inserted_timestamp'}
      for col in columns:
          if col not in valid_columns:
              raise ValueError(f"Invalid column name: {col}")
              
      # Build the query
      query_columns = ', '.join(columns)
      query = f"SELECT {query_columns} FROM air_quality"
      params = []
        
      # Filter for the last x days
      if last_days is not None:
            start_date = datetime.datetime.now() - datetime.timedelta(days=last_days)
            query += " WHERE time >= %s"
            params.append(start_date)
            
      # Run query
      c = conn.cursor()
      c.execute(query, params)
      data = c.fetchall()
      df = pd.DataFrame(data, columns=columns)
      c.close()
      
      return df
    
    
  def insert_data(self, conn, data):
      if conn is None:
          print('Not connected to db')
          return
   
      # Query to insert values           
      query_values = '''INSERT INTO air_quality (city, time, aqi, inserted_timestamp)
                 VALUES (%s, %s, %s, %s)
                 ON CONFLICT (city, time)
                 DO UPDATE SET aqi = EXCLUDED.aqi, inserted_timestamp = EXCLUDED.inserted_timestamp
                 WHERE air_quality.aqi IS NULL AND EXCLUDED.aqi IS NOT NULL'''

      c = conn.cursor()

      for index, row in data.iterrows():
          # Assuming 'city' is defined somewhere, if it's a part of 'data', use row['city']
          values = (row['city'], row['time'], row['aqi'], row['inserted_timestamp'])

          try:
              c.execute(query_values, values)
          except Exception as e:
              print(f"Error inserting row {index}: {e}")
              conn.rollback()
      c.close()

# ----------------- To remove in prod -----------------
# dbmanager_instance = DatabaseManager(connection_string)
# conn = dbmanager_instance.create_connection()
# aqi_api = AqiAPI(token)
# city = 'Barcelona'
# data = aqi_api.extract_data(city)
#dbmanager_instance.insert_data(conn,data)
 # data
