# Basic libraries
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers

class Model():
  
  def __init__(self):
      self.model = None
      
  def build_model(self) -> None:
      model = Sequential()
      model.add(layers.Input((3,1)))
      model.add(layers.LSTM(64))
      model.add(layers.Dense(units=32, activation="relu"))
      model.add(layers.Dense(units=32, activation="relu"))
      model.add(layers.Dense(1))
      model.compile(
          optimizer="Adam", loss="mse", metrics=["mean_absolute_error"]
      )
      self.model = model

# ----------------- To remove in prod -----------------
# my_model = Model()
# my_model.build_model()

