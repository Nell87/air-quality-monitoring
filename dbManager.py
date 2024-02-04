import requests
import os
import configparser
import psycopg2 
import pandas as pd

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
          
  def get_airquality_city(self,conn):
    
      query = "SELECT city, time, aqi FROM air_quality"
      c = conn.cursor()
      c.execute(query)
      data = c.fetchall()
      df = pd.DataFrame(data,columns=['city', 'time', 'aqi', 'inserted_timestamp'])
      c.close()
      return df
    
    
  def insert_data(self,conn, data):
    if conn is None:
      print('Not connected to db')
      return
    
    else:
      query = 'INSERT INTO air_quality (city, time, aqi, inserted_timestamp) VALUES (%s, %s, %s, %s) ON CONFLICT (city, time) DO NOTHING'
      
      c = conn.cursor()
      for index, row in data.iterrows():
        values = (row['city'], row['time'], row['aqi'],row['inserted_timestamp'])
      
      try:
        c.execute(query, values)
        
      except Exception as e:
        print(f"Error inserting row {index}: {e}")
        conn.rollback()
    
    conn.commit()
    print('Data inserted')
    
    c.close()

# dbmanager_instance = DatabaseManager(connection_string)
# conn = dbmanager_instance.create_connection()  
# data = dbmanager_instance.get_airquality_city(conn)
# dbmanager_instance.insert_data(conn,data)
# data
