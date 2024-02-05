import requests
import datetime
import datetime
import pandas as pd
import os

class AqiAPI:
  """ Data extraction from the aqicn API 
  https://aqicn.org/api/
  """
  def __init__(self, token):
    self.token = token
  
  def extract_data(self,city):
    # api conection
    api_connection = f"https://api.waqi.info/feed/{city}/?token={self.token}"
    response = requests.get(api_connection)
    
    if response.status_code == 200:
      data = response.json()
      
      # Extracting the AQI and time data
      air_quality_data_aqi = data["data"]["aqi"]
      air_quality_data_time = data["data"]['time']['s']
      
      # Creating a DF
      df = pd.DataFrame({
        'city' : [city], 
        'aqi' : [air_quality_data_aqi],
        'time' : [air_quality_data_time],
        'inserted_timestamp' :  datetime.datetime.now() 
      })
      
      return df
    
    else:
      return {"error": f"Failed to get data"}
    
# ----------------- To remove in prod -----------------
# aqi_api = AqiAPI(token)
# city = 'Barcelona'
# data = aqi_api.extract_data(city)
# print(data)

