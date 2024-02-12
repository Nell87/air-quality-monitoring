# Basic libraries
import tensorflow as tf
import numpy as np
import pandas as pd
import datetime as dt

class Predict():
  def __init__(self, trained_model_path, sequence_length):
    self.model = tf.keras.models.load_model(trained_model_path)
    self.sequence_length = sequence_length
    
  def predict(self, X):
    return self.model.predict(X)

  def forecast(self, initial_sequence, steps=1):
    current_sequence = np.array(initial_sequence).reshape((1, self.sequence_length, 1))

    predictions = []

    for _ in range(steps):
        # Predict the next step
        predicted_value = self.model.predict(current_sequence)[0][0]
        predictions.append(predicted_value)
        
        # Update the sequence with the predicted value
        current_sequence = np.roll(current_sequence, -1, axis=1)
        current_sequence[0, -1, 0] = predicted_value
        
    return predictions
    
  
  def dictionary_to_df(predictions):
    rows = [] 
    for city, info in predictions.items():
      for datetime, value in zip(info['predictions_date'], info['real_predictions']):
          rows.append({'City': city, 'Time': datetime, 'Prediction': value})
          
    df = pd.DataFrame(rows) 
    df['inserted_timestamp'] = dt.datetime.now().replace(microsecond=0)
    return df
      
#df_dates_predictions(real_predictiosn, dates)
# ----------------- To remove in prod -----------------
# sequence_length = 3
# initial_sequence = [0.5] * sequence_length
# model_forecast= Predict("./models/keras.h5", sequence_length=sequence_length)
# real_predictions = model_forecast.forecast(initial_sequence, steps=5)
# real_predictions
