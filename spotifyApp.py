import streamlit as st
from google.cloud import storage
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
import datetime


st.title("Hello, Streamlit!")
st.write('''
# Spotify Streaming History
''')

storage_client = storage.Client()
bucket_name = 'streaminghistory'
bucket = storage_client.get_bucket(bucket_name)

# Prefix to filter files
prefix = 'MyData2/Streaming_History'
dfs = []
# List blobs (files) in the bucket with the specified prefix
blobs = bucket.list_blobs(prefix=prefix)

# Collect the file names
file_names = [blob.name for blob in blobs]

for i in range(len(file_names)):
  file_name = file_names[i]
  local_file_name = "StreamingHistory"+str([i][0])+".json"
  #print(local_file_name)
  #print(file_name)
  blob = bucket.blob(file_name)
  blob.download_to_filename(local_file_name)
  df = pd.read_json(local_file_name)
  dfs.append(df)
combined_df = pd.concat(dfs, ignore_index=True)

combined_df['timestamp'] = pd.to_datetime(combined_df['ts'])
combined_df['timestamp'] =pd.to_datetime(combined_df['timestamp'].dt.floor('d')).dt.strftime('%Y-%m-%d')


#combined_df['timestamp'] = datetime.datetime.fromtimestamp(combined_df['ts'])

#pd.to_datetime(combined_df['ts'].str.replace(r'\[.*\]', '', regex=True),format='ISO8601')

#v = datetime.datetime.fromtimestamp(v)

min_time = datetime.strptime(combined_df["timestamp"].min(), '%Y-%m-%d').date()
max_time = datetime.strptime(combined_df["timestamp"].max(), '%Y-%m-%d').date()

#min_time = pd.to_datetime(combined_df["timestamp"].min())
#max_time = pd.to_datetime(combined_df["timestamp"].max())

print(type(min_time))
print(type(max_time))

st.write(f"From {min_time} to {max_time}")

filter_value = st.slider('Select a threshold for x', min_value=min_time, max_value=max_time, value=min_time)

filtered_df = combined_df[combined_df['timestamp'] > filter_value]

st.dataframe(combined_df)



