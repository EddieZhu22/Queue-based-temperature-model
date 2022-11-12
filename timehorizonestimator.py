import matplotlib
import numpy as np
import csv
import pandas as pd 


# making dataframe 
df = pd.read_csv("data3.csv") 
tempdiff = []
t0list = []
t3list = []

def findt0t2t3():
    
    # Find maximum "Queue"
    
    t2 = df[df['Average of Temperature'] == df['Average of Temperature'].max()].index.to_list()[0]
    print('t2: ' + str(t2))
    
    # Eqn 6: t2 = 1/3t0 + 2/3t3
    # back calculate t0/t3 (t2 - 1/3t0 = 2/3t3)
    for dist in range(t2):
        t0 = t2 - dist
        t3 = (t2 - 1/3*t0)*(3/2)
        if(t3.is_integer()):
            print('t0: ' + str(t0) + ' t3: ' + str(t3))
            tempdiff.append(df['Average of Temperature'][t3] - df['Average of Temperature'][t0])
    print(tempdiff)
def findtempcuttoff():
    tempmin = []
    t0s = []
    t3s = []
    for i in np.arange(int(len(df['Average of Temperature'])/2)):
        for k in np.arange(len(df['Average of Temperature'])/2):
            t3 = df[df['Average of Temperature'] == df['Average of Temperature'][df['Average of Temperature'].count() - 1 - k]].index.to_list()[0]
            t0 = df[df['Average of Temperature'] == df['Average of Temperature'][i]].index.to_list()[0]
            if(t0 != t3):
                tempmin.append(abs(df['Average of Temperature'][t3] - df['Average of Temperature'][t0]))
                t0s.append(t0)
                t3s.append(t3)
        tempminkey = tempmin.index(min(tempmin))
        tempdiff.append(min(tempmin))
        t0list.append(t0s[tempminkey])
        t3list.append(t3s[tempminkey])
        tempmin.clear()
        t0s.clear()
        t3s.clear()
        print(str(i/int(len(df['Average of Temperature'])/2)*100) + '%')
    print('smallest temperature difference: ' + str(min(tempdiff)))
    tempdiffkey = tempdiff.index(min(tempdiff))
    t0final = t0list[tempdiffkey]
    t3final = t3list[tempdiffkey]
    print("t0: " + str(t0final))
    print("t3: " + str(t3final))
    
    
    # Find t2  
    # Eqn 6: t2 = 1/3t0 + 2/3t3
    t2 = 1/3 * t0final + 2/3 * t3final
    print("t2: " + str(t2))
    
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
        

if __name__=="__main__":
    #findt0t2t3()
   # findtempcuttoff()
    mfactor(440,1080)