# Running the data pipeline
from pathlib import Path
from extract import AqiAPI
from dbManager import DatabaseManager
from preprocess import Preprocess
import os
import requests
import psycopg2 
import pandas as pd
from config import dbparam, token, cities, connection_string

def main():
  # Initialize your API and Database instance
  dbmanager_instance = DatabaseManager(connection_string)
  conn = dbmanager_instance.create_connection()
  
  # Extract
  columns = ['time', 'city', 'aqi']
  data = dbmanager_instance.get_airquality_info(conn,columns, 1)
    
  # Create a dataset per city
  city_datasets = Preprocess.split_data_by_city(data)
  
  for city, dataset in city_datasets.items():
    #  ----------------- Preprocess pipeline -----------------
    # Replace outliers with NA
    clean_data = Preprocess.replace_outliers_withNA(dataset, col_name = 'aqi') 
    filled_data = Preprocess.fill_noregisters_withNA(clean_data, col_name = 'time')
    
    # Impute Nas
    filled_data_NA = Preprocess.impute_NA(filled_data, col_name = 'time')

    # Normalize data
    data_norm = Preprocess.rescale(data, col_name = 'aqi')
    city_datasets[city] = data
    
    #  ----------------- Training pipeline -------------------
  
  return city_datasets
    
  
  conn.close()
  
data_no_outliers = main()
