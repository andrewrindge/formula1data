import pandas as pd
import json
import requests

# query API

url = "http://ergast.com/api/f1/"

CURR_DRIVERS = ['alonso', 'verstappen', 'ricciardo', 'norris', 'vettel', 'latifi', 'gasly', 'perez', 
'leclerc', 'stroll', 'magnussen', 'tsunoda', 'albon', 'ocon', 'hamilton', 'guanyu', 'sainz',
'schumacher', 'russell', 'bottas']

ACC = [3, 4, 104]

df_drivers = pd.DataFrame() #blank dataframe object
for driver in CURR_DRIVERS:
    for val in ACC:
      try:
        dataset = url + "/drivers/" + str(driver) +  "/status/" + val + ".json?limit=200"
        subset = pd.DataFrame.from_dict(json.loads(requests.get(dataset).text)["MRData"]["StatusTable"]["Status"])
        subset['val'] = val
        frames = [df_drivers, subset]
        df_drivers = pd.concat(frames)
      except:
        df_drivers = pd.concat(None)
        
df_drivers["count"] = pd.to_numeric(df_drivers["count"])        
df_drivers = df_drivers.groupby(["val"]).sum().sort_index()

# df_drivers.to_csv(r'/Users/andrewrindge/School/Formula_1_267/data_collection/accidentsperdriver.csv', index=False)