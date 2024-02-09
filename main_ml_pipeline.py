# Running the data pipeline
from pathlib import Path
from extract import AqiAPI
from dbManager import DatabaseManager
from preprocess import Preprocess
from train import Train
from model import Model
from predict import Predict
import os
import requests
import psycopg2 
import pandas as pd
from config import dbparam, token, cities, connection_string
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
import tensorflow as tf

# set random seed for reproducibility
tf.random.set_seed(314)

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
    # Replace outliers with NA
    clean_data = Preprocess.replace_outliers_withNA(dataset, col_name = 'aqi') 
    filled_data = Preprocess.fill_noregisters_withNA(clean_data, col_name = 'time')
    
    # Impute Nas
    filled_data_NA = Preprocess.impute_NA(filled_data, col_name = 'time')

    # Normalize data
    #data_norm = Preprocess.rescale(filled_data_NA, col_name = 'aqi')  
    
    # Reshape data for LSTM
    windowed_data = Preprocess.window_data(filled_data_NA,'aqi', n=3)
    
    # Split in dates, x, y
    dates, X, y = Train.Windowed_data_to_data_x_y(windowed_data)
  
    #  ----------------- Training pipeline -------------------
    # Train / test
    train_instance = Train()
    train_instance.Train_test_split(windowed_data, dates, X, y)
    
    # Initialize and fit the model
    train_instance.Init_model()
    train_instance.Fit_model()
    
    # Save model
    train_instance.save_model()
    
    # Predictions
    sequence_length = 3
    initial_sequence = [0.5] * sequence_length
    
    model = Predict("./models/keras.h5",sequence_length = sequence_length)
    train_predictions = model.predict(train_instance.X_train).flatten()
    val_predictions = model.predict(train_instance.X_val).flatten()
    test_predictions = model.predict(train_instance.X_test).flatten()
    

    model_forecast= Predict("./models/keras.h5", sequence_length=sequence_length)
    real_predictions = model_forecast.forecast(initial_sequence, steps=5)

    predictions[city] = {
            'train_predictions': train_predictions,
            'val_predictions': val_predictions,
            'test_predictions': test_predictions,
            'real_predictions':real_predictions
            }
    
  return predictions
    
  conn.close()
  
predictions = main()
