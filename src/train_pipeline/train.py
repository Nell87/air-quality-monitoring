from dbManager import DatabaseManager
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from model import Model
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers

class Train():
  
  def __init__(self):
      self.model = None
      self.X_train = None
      self.y_train = None
      self.X_val = None
      self.y_val = None
      self.X_test = None
      self.y_test = None
      self.dates_train = None
      self.dates_val =  None
      self.dates_test = None
      
  def Windowed_data_to_data_x_y(data):
      dates = data.index
      middle_matrix = data.iloc[:, :-1].to_numpy()
      X = middle_matrix.reshape((len(dates), middle_matrix.shape[1], 1))
      Y = data.iloc[:, -1].to_numpy()
        
      return dates, X.astype(np.float32), Y.astype(np.float32)
    
  def Train_test_split(self,data, dates, X, y):
    q80 =int(len(dates) * 0.8)
    q90 =int(len(dates) * 0.9)
    
    self.dates_train, self.X_train, self.y_train = dates[:q80], X[:q80], y[:q80]
    self.dates_val, self.X_val, self.y_val = dates[q80:q90], X[q80:q90], y[q80:q90]
    self.dates_test, self.X_test, self.y_test = dates[q90:], X[q90:], y[q90:]
    
  def Init_model(self):
      self.model_instance = Model()
      self.model_instance.build_model()
      self.model = self.model_instance.model
      
      
  def Fit_model(self):
      self.model.fit(
        self.X_train,
        self.y_train,
        validation_data = (self.X_val, self.y_val),
        epochs = 2
      )
      
  def save_model(self):
        """Save model in SavedModel format"""
        tf.saved_model.save(self.model, './models/SavedModel')

        """Save model in Keras format"""
        self.model.save('./models/keras.h5')
      
  def predict(self, X):
    return self.model.predict(X)

# ----------------- To remove in prod -----------------
# # create and fit the LSTM network
# model = Sequential()
# model.add(LSTM(4, input_shape=(1, look_back)))
# model.add(Dense(1))
# model.compile(loss='mean_squared_error', optimizer='adam')
# model.fit(trainX, trainY, epochs=100, batch_size=1, verbose=2)
# 
# 
# # make predictions
# trainPredict = model.predict(trainX)
# testPredict = model.predict(testX)
# # invert predictions
# trainPredict = data_scale.inverse_transform(trainPredict)
# trainY = data_scale.inverse_transform([trainY])
# testPredict = data_scale.inverse_transform(testPredict)
# testY = data_scale.inverse_transform([testY])
# # calculate root mean squared error
# trainScore = np.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
# print('Train Score: %.2f RMSE' % (trainScore))
# testScore = np.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
# print('Test Score: %.2f RMSE' % (testScore))


