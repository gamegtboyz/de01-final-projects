def load_and_clean():
    import requests
    import pandas as pd
    import json
    
    # setup endpoints and API key
    endpoints = "https://data.cityofnewyork.us/resource/h9gi-nx95.json"
    token = "qMLbbltM4PxnOZ6W4yZgE3QIO"

    # define parameters
    params = {
        '$limit' : 10000,
        '$offset' : 0,
        '$where' : 'crash_date >= "2022-01-01T00:00:00"',
        '$order' : 'crash_date DESC',
    }

    # set headers
    headers = {
        'X-App-Token' : token
    }

    # fetch data
    all_data = []
    i = 0
    while True:
        response = requests.get(endpoints,headers = headers, params = params)

        if response.status_code == 200:
            data = response.json()

            # if there's no more data, then break it 
            if not data:
                break

            all_data.extend(data)
            params['$offset'] += len(data)
            i += 1
            print(f'fetching ({i})')
        else:
            print(f'Error: {response.status_code}, {response.text}')
            break

    # convert the downloaded data from json to DataFrame, then export it into .csv files
    df = pd.DataFrame(all_data)

    # drop the location column
    df.drop(['location'], axis = 1, inplace = True)

    # drop the null values in some columns
    df.dropna(subset = ['contributing_factor_vehicle_1','vehicle_type_code1','latitude','longitude'], inplace = True)

    # drop the observations with 0,0 coordinates
    df.drop(df[(df['latitude'] == 0) & (df['longitude'] == 0)].index, inplace = True)

    # exported the cleaned data onto new .csv files
    df.to_csv('nyc-collisions.csv',index = False)
    print(f"{i} page(s) of dataset were downloaded successfully.")