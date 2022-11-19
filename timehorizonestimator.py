import numpy as np
import pandas as pd 


# making dataframe 
df = pd.read_csv("datasets/data3.csv") 


def findt0t2t3(array, cuttoff):
    t0dist = []
    t3dist = []
    for i in np.arange(int(len(array)/2)):
        t0dist.append(abs(array[i] - cuttoff))
    for i in np.arange(int(len(array)/2),len(array)):
        t3dist.append(abs(array[i] - cuttoff))
        
    #print(t0dist)
    #print(t3dist)
    t0 = t0dist.index(min(t0dist)) * 10
    t3 = (t3dist.index(min(t3dist)) + int(len(array)/2)) * 10
    
    return t0, t3
    
def mfactor(t0,t3): 
    # compare maximum queue (max temperature) with the theoretical m value 2/3. 
    # Finds both percent difference and absoulute difference between the t2 and m value
    
    m = 2/3
    t2 = t0+m*(t3-t0)
    print(t2)
    # First find each day from large list of datapoints
    # Each day is 1440 minutes long
    day = 0
    temperatureArr = []
    temperatureTimeArr = []
    for i in np.arange(int(len(df['Minute']))):
        if(df['Minute'][i] % 1440 == 0):
            if(day > 0):
                
                #find the maximum temperature through maxing the index.
                tempmaxkey = temperatureArr.index(max(temperatureArr))
                temperatureTimeArr[tempmaxkey]
                
                #normalize per day duration
                tempmaxtime = temperatureTimeArr[tempmaxkey] - (day-1)*1440
                
                #absoulute time difference
                temptime_absdiff = abs(t2 - tempmaxtime)
                
                #relative time difference
                calculated_m =  (tempmaxtime - t0)/(t3-t0)
                temptime_reldiff  = (abs(calculated_m - m) / ((calculated_m + m) /2))*100
                print(calculated_m)
                temperatureArr.clear()
                temperatureTimeArr.clear()
            day += 1

        temperatureArr.append(df['Average of Temperature'][i])
        temperatureTimeArr.append(df['Minute'][i])
        