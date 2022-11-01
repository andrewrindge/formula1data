import pandas as pd
import json
import requests

# query API

url = "http://ergast.com/api/f1/"
FINISHED = [1]
df_fin = pd.DataFrame() #blank dataframe object
for code in FINISHED:
    for yr in range(2000,2021):
      try:
        dataset = url + str(yr) + "/status/" + str(code) + ".json?limit=200"
        subset = pd.DataFrame.from_dict(json.loads(requests.get(dataset).text)["MRData"]["StatusTable"]["Status"])
        subset['year'] = yr
        frames = [df_fin, subset]
        df_fin = pd.concat(frames)
      except:
        df_fin = pd.concat(None)
        
df_fin["count"] = pd.to_numeric(df_fin["count"])        
df_fin = df_fin.groupby(["year"]).sum().sort_index()

ACCIDENT = [2,3,104]
df_acc = pd.DataFrame() #blank dataframe object
for code in ACCIDENT:
    for yr in range(2000,2021):
      try:
        dataset = url + str(yr) + "/status/" + str(code) + ".json?limit=200"
        subset = pd.DataFrame.from_dict(json.loads(requests.get(dataset).text)["MRData"]["StatusTable"]["Status"])
        subset['year'] = yr
        frames = [df_acc, subset]
        df_acc = pd.concat(frames)
      except:
        df_acc = pd.concat(None)
        
df_acc["count"] = pd.to_numeric(df_acc["count"])        
df_acc = df_acc.groupby(["year"]).sum().sort_index()

DNF = [31, 54]
df_dnf = pd.DataFrame() #blank dataframe object
for code in DNF:
    for yr in range(2000,2021):
      try:
        dataset = url + str(yr) + "/status/" + str(code) + ".json?limit=200"
        subset = pd.DataFrame.from_dict(json.loads(requests.get(dataset).text)["MRData"]["StatusTable"]["Status"])
        subset['year'] = yr
        frames = [df_dnf, subset]
        df_dnf = pd.concat(frames)
      except:
        df_dnf = pd.concat(None)
        
df_dnf["count"] = pd.to_numeric(df_dnf["count"])        
df_dnf = df_dnf.groupby(["year"]).sum().sort_index()

df_fin = df_fin.rename(columns={'count': 'Finishes'})
df_acc = df_acc.rename(columns={'count': 'Accidents'})
df_dnf = df_dnf.rename(columns={'count': 'DNF'})

results = pd.concat([df_fin, df_dnf, df_acc], axis=1, sort=False)
results = results.fillna(0)

results.to_csv(r'/Users/andrewrindge/School/Formula_1_267/data_collection/finishingstatus.csv', index=False)