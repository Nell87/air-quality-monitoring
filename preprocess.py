from config import dbparam, token, cities, connection_string
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class Preprocess():
  
  def __init__(self)-> None:
      self.attribute: str = "Initial Value"

  def split_data_by_city(data):
      city_datasets = {city: city_group.drop('city', axis=1).reset_index(drop=True) 
                       for city, city_group in data.groupby('city')}
      return city_datasets

  def replace_outliers_withNA(data, col_name): 
    # Calculate bounds
    col_name = 'aqi'
    lower_bound = data[col_name].median() - 3 * data[col_name].std()
    upper_bound = data[col_name].median() + 3 * data[col_name].std()
    
    # Replace outliers with NAs using Standard Deviation.
    data[col_name] = data[col_name].apply(lambda x: np.nan if x < lower_bound or x > upper_bound else x)
    return data
  
  def fill_noregisters_withNA(data, col_name): 
    data.set_index(col_name, inplace=True)
    date_range = pd.date_range(start=data.index.min(), end=data.index.max(), freq='H')
    data_complete = data.reindex(date_range)
    
    data_complete.reset_index(inplace=True)
    data_complete.rename(columns={'index': col_name}, inplace=True)

    return data_complete

  def impute_NA(data, col_name): 
    # Imputing with linear interpolation
    data.set_index(col_name, inplace=True)
    linear_interpolation = data.interpolate(method='linear')
    return linear_interpolation
  
  def rescale(data, col_name):
    # Prepare the array
    array = data[col_name].values.reshape(-1, 1)  # Reshape from 1D to 2D
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled = scaler.fit_transform(array)
    data[col_name] = scaled.flatten()
    
    return data
  
  def window_data(data,col_name, n=3):
      windowed_data = pd.DataFrame()
      for i in range(n, 0, -1):
          windowed_data[f'Target-{i}'] = data[col_name].shift(i)
      windowed_data['Target'] = data[col_name]
      return windowed_data.dropna()
    
# ----------------- To remove in prod -----------------
# dbmanager_instance = DatabaseManager(connection_string)
# conn = dbmanager_instance.create_connection()
# columns = ['time', 'city', 'aqi']
# data = dbmanager_instance.get_airquality_info(conn,columns, 3)
# data_bcn = data.loc[data['city'] == 'Barcelona']
# test = Preprocess.replace_outliers_withNA(data_bcn, col_name = 'aqi')
# test
