import numpy as np
import pandas as pd 
import warnings
import os
# Determine If latitude/longitude is within maricopa/pinal county 


#df = pd.read_csv('RawData/2019/' + 'GriddedDataSetPoint1178595.csv', dtype=object)
i = 0
lats = []
longs = []
ids = []
for root, dirs, files in os.walk('RawData/2019/'):
    for file in files:
        if file.endswith('.csv'):
            i+=1
            print(i)
            if(file == 'GriddedDataSetPoint1204421_2019.csv'or file == 'GriddedDataSetPoint1202785_2019.csv'or file == 'GriddedDataSetPoint1201171_2019.csv'or file == 'GriddedDataSetPoint1206057_2019.csv'):
                df = pd.read_csv('RawData/2019/' + str(file), dtype=object)
                print(file)
                #print(f"Latitude: {df['Latitude'][0]}")
                #print(f"Longitude: {df['Longitude'][0]}")
                lats.append(df['Latitude'][0])
                longs.append(df['Longitude'][0])
            
            else:
                df = pd.read_csv('RawData/2019/' + str(file), dtype=object)
                #print(file)
                #print(f"Latitude: {df['5'][1]}")
                #print(f"Longitude: {df['6'][1]}")
                lats.append(df['5'][1])
                longs.append(df['6'][1])
            ids.append(file)
                
                

list_of_tuples = list(zip(ids, lats, longs))    
pd.DataFrame(list_of_tuples, columns=['FileName','Lat', 'Long']).to_csv('LatitudeLongitude.csv')