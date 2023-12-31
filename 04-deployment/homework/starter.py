#!/usr/bin/env python
# coding: utf-8


# In[1]:


import pickle
import pandas as pd
import sys


# In[2]:


with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)
    print('Success model.bin loaded.')


# In[3]:


categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


# In[4]:

def apply_model(df):
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)
    df['predicted_duration'] = y_pred
    return df


# In[5]:

def run():
    taxi_type = sys.argv[1]
    year = int(sys.argv[2])
    month = int(sys.argv[3])
    df = read_data(f'https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet')
    df = apply_model(df)
    print(df.predicted_duration.mean())
    df.to_parquet('result', index=False)
    return df

if __name__ == '__main__':
    run()
    

