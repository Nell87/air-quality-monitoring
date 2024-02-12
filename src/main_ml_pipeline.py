# Basic libraries
import os
import requests
import psycopg2 
import pandas as pd
import sys
import datetime
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
import tensorflow as tf

# Paths 
sys.path.append(os.path.abspath('./data_pipeline/'))
sys.path.append(os.path.abspath('./preprocess_pipeline/'))
sys.path.append(os.path.abspath('./train_pipeline/'))
sys.path.append(os.path.abspath('./prediction_pipeline/'))

# Own libraries
from extract import AqiAPI
from dbManager import DatabaseManager
from preprocess import Preprocess
from train import Train
from model import Model
from predict import Predict
from config import dbparam, token, cities, connection_string
from preprocess_pipeline import preprocess_pipeline

# set random seed for reproducibility
tf.random.set_seed(314)

# Running the pipeline
def main():
  # Initialize your API and Database instance
  dbmanager_instance = DatabaseManager(connection_string)
  conn = dbmanager_instance.create_connection()
  
  # Extract
  columns = ['time', 'city', 'aqi']
  data = dbmanager_instance.get_airquality_info(conn,columns, 5)
    
  # Create a dataset per city
  city_datasets = Preprocess.split_data_by_city(data)
  
  # Initialize a dictionary
  predictions = {}
  
  for city, dataset in city_datasets.items():
    #  ----------------- Preprocess pipeline -----------------
    preprocess_instance = Preprocess()
    processed_data = preprocess_instance.run_preprocess(dataset)
    
    #  ----------------- Training pipeline -------------------
    # Split in dates, x, y
    dates, X, y = Train.Windowed_data_to_data_x_y(processed_data)

    # Train / test
    train_instance = Train()
    train_instance.Train_test_split(processed_data, dates, X, y)

    # Initialize and fit the model
    train_instance.Init_model()
    train_instance.Fit_model()

    # Save model
    train_instance.save_model()

    #  ----------------- Predicting pipeline -------------------
    sequence_length = 3
    initial_sequence = [0.5] * sequence_length

    model = Predict("./models/keras.h5",sequence_length = sequence_length)
    train_predictions = model.predict(train_instance.X_train).flatten()
    val_predictions = model.predict(train_instance.X_val).flatten()
    test_predictions = model.predict(train_instance.X_test).flatten()

    model_forecast= Predict("./models/keras.h5", sequence_length=sequence_length)
    real_predictions = model_forecast.forecast(initial_sequence, steps=5)
    
    # Get forecasting date
    dates_df = pd.DataFrame(dates, columns=['time'])      
    last_date = pd.to_datetime(dates_df.iloc[-1]['time'])
    next_hour_start = last_date + pd.Timedelta(hours=1)

    n= len(real_predictions)
    pred_dates = pd.date_range(start=next_hour_start, periods=n, freq='H')
    
    # Final dataset
    predictions[city] = {
            #'train_predictions': train_predictions,
            #'val_predictions': val_predictions,
            #'test_predictions': test_predictions,
            'predictions_date':pred_dates,
            'real_predictions':real_predictions
            }

  df = Predict.dictionary_to_df(predictions)
  
  #  ----------------- Storing predictions in db -------------------
  dbmanager_instance = DatabaseManager(connection_string)
  conn = dbmanager_instance.create_connection()
  dbmanager_instance.insert_pred(conn,df)

  return df
    
  conn.close()
  
predictions = main()
