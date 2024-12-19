# import relevant packages
import pandas as pd
import numpy as np

# read the download datasets in .csv format
data = pd.read_csv('nyc-collisions.csv')

# drop the location column
data.drop(['location'], axis = 1, inplace = True)

# drop the null values in some columns
data.dropna(subset = ['contributing_factor_vehicle_1','vehicle_type_code1','latitude','longitude'], inplace = True)

# drop the observations with 0,0 coordinates
data.drop(data[(data['latitude'] == 0) & (data['longitude'] == 0)].index, inplace = True)