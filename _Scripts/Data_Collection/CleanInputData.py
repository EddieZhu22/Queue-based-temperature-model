import pandas as pd
import os
import shutil
import numpy as np
i = 0

df = pd.read_csv('Area.csv')

for root, dirs, files in os.walk('RawData/2019/'):
    for file in files:
        if file.endswith('.csv'):           
            if(df['Yes'][i] == 0):
                df1 = pd.read_csv('RawData/2019/' + str(file), dtype=object)
                if os.name == 'nt':    #check if windows 
                    a='\\'
                else:
                    a='/'

                original = "D:"+a+"Projects"+a+"ASU"+a+"TemperatureResearch"+a+"RawData"+a+"2019"+a+file
                target = "D:"+a+"Projects"+a+"ASU"+a+"TemperatureResearch"+a+"RawData"+a+"archived"+a+file
                shutil.move(original, target)
            i+=1
            

fileName = 'RawData/2019/GriddedDataSetPoint1201095_2019.csv'
columns = ['','Year','Month','Day','Hour','Minute','GHI','Temperature']            
print(columns[1:7])
global is_special
is_special = False
#df = pd.read_csv('datasets/1343797_35.20_-111.65_2019.csv', sep=",", header=None, low_memory=False,error_bad_lines=False, index_col=False, dtype=object)
def data_pre_processing(fileName):
    if(file == 'GriddedDataSetPoint1204421_2019.csv'or file == 'GriddedDataSetPoint1202785_2019.csv'or file == 'GriddedDataSetPoint1201171_2019.csv'or file == 'GriddedDataSetPoint1206057_2019.csv'):
        print('funny')
        global is_special
        is_special = True
        df = pd.read_csv(fileName, header=None, names=columns[1:8], usecols=columns[1:8], dtype=object,
            delimiter=',', lineterminator='\n', skiprows=3).reset_index(drop=True)
        df = df.drop(columns=['Year','Month','Day','Hour','Minute'])
    #else:
     #   df = pd.read_csv(fileName, header=None, names=columns, usecols=columns, dtype=object,
        #   delimiter=',', lineterminator='\n', skiprows=4).reset_index(drop=True)
      #  df = df.drop(columns=['','Year','Month','Day','Hour','Minute'])

        df.insert(0,'Minute', np.arange(0, len(df) * 10, 10))
    #print(df)
        return df
i = 0
for root, dirs, files in os.walk('RawData/2019/'):
    for file in files:
        if file.endswith('.csv'):    
            df = data_pre_processing("RawData/2019/" + file)
            if(is_special == True):
                df.to_csv('datasets/CleanedData/2019/' + file)
            is_special = False
            print(file + ' processed')
            i += 1