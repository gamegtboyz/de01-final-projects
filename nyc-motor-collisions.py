import requests
import pandas as pd
import json
# setup endpoints and API key
endpoints = "https://data.cityofnewyork.us/resource/h9gi-nx95.json"
token = "qMLbbltM4PxnOZ6W4yZgE3QIO"

# define parameters
params = {
    '$limit' : 1000,
    '$offset' : 0,
    '$where' : 'crash_date >= "2024-01-01T00:00:00"',
    '$order' : 'crash_date DESC',
}

# set headers
headers = {
    'X-App-Token' : token
}

# fetch data
all_data = []
while True:
    response = requests.get(endpoints,headers = headers, params = params)

    if response.status_code == 200:
        data = response.json()
        # if there's no more data, then break it 
        if not data:
            break

        all_data.extend(data)
        params['$offset'] += len(data)
    else:
        print(f'Error: {response.status_code}, {response.text}')
        break

# convert the downloaded data from json to DataFrame, then export it into .csv files
df = pd.DataFrame(all_data)
df.to_csv('nyc-collisions.csv',index = False)
print("Dataset was downloaded successfully.")