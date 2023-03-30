# Import required packages
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
import sys
import os
import time
import multiprocessing as mp
from sklearn.linear_model import LinearRegression

# Add a directory to the system path
sys.path.append('/_Scripts')

# Define a constant variable
MIN_IN_YR = 525600

# Create an empty list to hold data
df = []

# Initialize input variables
g_num_years = [1,0,0]
g_start_day = 172
g_end_day = 265
g_cuttoff = 38.02525708
dataset_num = 0

# Initialize statistics visualization variables
g_Queues = []
g_Lambdas = []
g_Mus = []

g_Mus_eq = []
eqn_queue = []
q_obs = []
g_temp_arr = []
g_ps = []
g_max_temp_arr = []
g_avg_temp_arr = []
tempdiff_arr = []
g_mtis = []
avg_lambda = []
DC_arr = []
D_arr = []
C_arr = []
avg_mu_arr = []
muOC_arr = []
mu_diff = []
day_num_arr = []
year_num_arr = []
day_arr = list(range(g_start_day, (g_end_day+1)))
p = 0


def findcutoff(data):
    print(f'CuttoffTemp')
    day = 0
    year = 0
    temperatureDayArr = []
    # Loop through the data, grouping it into days.
    for i in range(1):
        for i in np.arange(((g_start_day * 144) - 144) + year * MIN_IN_YR/10, (g_end_day * 144)+1+ year * MIN_IN_YR/10):
            if (data['Minute'][i] % 1440 == 0):
                if (day > 0):
                    g_temp_arr.append(np.min(temperatureDayArr))
                temperatureDayArr.clear()
                day += 1
            temperatureDayArr.append(float(data['Temperature'][i]))
            #print(temperatureDayArr)
        year += 1
        day = 0

def QueueBasedTemperatureModel(data, file, timehorizon = 10):
    print('Running Model')
    day = 0
    year = 0
    temperatureDayArr = []
    GHIDayArr = []
    # Loop through the data, grouping it into days.
    for i in range(1):
        for i in np.arange(((g_start_day * 144) - 144) + year * MIN_IN_YR/10, (g_end_day * 144)+1+ year * MIN_IN_YR/10):
            if (data['Minute'][i] % 1440 == 0):
                if (day > 0):
                    g_max_temp_arr.append(max(temperatureDayArr))
                    g_avg_temp_arr.append(np.mean(temperatureDayArr))
                    t0, t3 = findt0t3(
                        temperatureDayArr, g_cuttoff)
                    mut0t2 = 0
                    sum_lambda = 0
                    netflow = 0
                    netflowt2t3 = 0
                    sum_netflow = 0
                    sum_mu = 0
                    sum_lambda = 0
                    slope = 1  # guessed
                    mu_arr = []
                    if(t0 > 0 and t3 > 0): 
                        t2 = int(1/3*t0 + 2/3 * t3)
                        p = (t3-t0)/60
                        tempdiff = max(temperatureDayArr) - g_cuttoff 
                        mti = ((max(temperatureDayArr) - g_cuttoff) / float(g_cuttoff)) * 100
                        #print(max(temperatureDayArr))
                        tempdiff_arr.append(tempdiff)
                        g_mtis.append(mti)
                        

                        # 0, t0
                        for k in np.arange(0, int(t0/timehorizon)):
                            mu_arr.append(0)
                            day_num_arr.append(day)
                            year_num_arr.append(year)
                            g_Queues.append(0)
                            g_Lambdas.append(0)
                            g_Mus.append(0)
                            g_Mus_eq.append(0)
                            
                        # t0 - t2
                        for k in np.arange(int(t0/timehorizon), int(t2/timehorizon)+1):
                                
                            mut0t2 = ((GHIDayArr[int(t2/timehorizon)]-GHIDayArr[int(t0/timehorizon)])/(
                                (t2-t0)/timehorizon))*(k-t0/timehorizon)+GHIDayArr[int(t0/timehorizon)]
                            mu_arr.append(mut0t2)
                            day_num_arr.append(day)
                            year_num_arr.append(year)
                            sum_mu += mut0t2
                            netflow = GHIDayArr[int(k)] - mut0t2
                            sum_netflow += netflow
                            
                            
                            g_Queues.append(sum_netflow)
                            g_Lambdas.append(GHIDayArr[int(k)])
                            g_Mus.append(mut0t2)
                        queue = sum_netflow

                        # total lambda for t2 t3
                        for k in np.arange(int(t2/timehorizon), int(t3/timehorizon)+1):
                            sum_lambda += GHIDayArr[int(k)]

                        # approximate slope
                        
                        slope = findmuslope(sum_netflow, GHIDayArr[int(int(t2/timehorizon))], GHIDayArr, sum_lambda, t2, t3)
                        #print(slope)
                        # total lambda for t0 t2
                        for k in np.arange(int(t0/timehorizon), int(t2/timehorizon)+1):
                            sum_lambda += GHIDayArr[int(k)]
                        # t2 - t3
                        #print(slope)
                        for k in np.arange(0, (int(t3/timehorizon)-int(t2/timehorizon))):
                            y = slope*k + GHIDayArr[int(int(t2/timehorizon))]
                            #print(GHIDayArr[int(t2/timehorizon) + k])
                            #print(y)
                            day_num_arr.append(day)
                            year_num_arr.append(year)
                            mu_arr.append(y)
                            sum_mu += y
                            netflowt2t3 = GHIDayArr[int(k) + int(t2/timehorizon)] - y
                            queue += netflowt2t3
                            #print(queue)
                            g_Queues.append(queue)
                            g_Lambdas.append(GHIDayArr[int(k) + int(t2/timehorizon)])
                            g_Mus.append(y)
                        if(t3 - t0 > 0):
                            avg_lambda.append((1 / (t3-t0)) * sum_lambda)
                        else:
                            avg_lambda.append(0)
                        
                            
                        mu_diff.append(
                            mu_arr[int(t2/timehorizon)] - mu_arr[0])
                        for k in np.arange(int(t3/timehorizon)-144, 0):
                            mu_arr.append(0)
                            day_num_arr.append(day)
                            year_num_arr.append(year)
                            g_Queues.append(0)
                            g_Lambdas.append(0)
                            g_Mus.append(0)
                            g_Mus_eq.append(0)
                            
                        # QTM Step 2.1 - Aggregate microscale results -> mesoscale
                        g_ps.append(p)
                        D_arr.append(sum_lambda)
                        C_arr.append(max(mu_arr))
                        mu_arr1 = [i for i in mu_arr if i != 0]
                        avg_mu_arr.append(np.mean(mu_arr1))
                        muOC_arr.append(np.mean(mu_arr1)/max(mu_arr))
                        DC_arr.append(sum_lambda/max(mu_arr))
                    else:
                        D_arr.append(0)
                        C_arr.append(0)
                        muOC_arr.append(0)
                        avg_mu_arr.append(0)
                        DC_arr.append(0)
                        g_ps.append(0)
                        g_mtis.append(0)
                        for k in np.arange(0, 144):
                            g_Mus_eq.append(0)
                            mu_arr.append(0)
                            day_num_arr.append(day)
                            year_num_arr.append(year)
                            g_Queues.append(0)
                            g_Lambdas.append(0)
                            g_Mus.append(0)
                temperatureDayArr.clear()
                GHIDayArr.clear()
                eqn_queue.clear()
                q_obs.clear()
                day += 1
            temperatureDayArr.append(float(data['Temperature'][i]))
            #print(temperatureDayArr)
            GHIDayArr.append(float(data['GHI'][i]))
        year += 1
        day = 0

        ExportData('PAQ', file)
        ExportData('QVDF', file)
        clearArrs()
def findmuslope(netflow, lambdat2,lambda_arr, total_lambda, t2, t3):
    total_mu = 0
    curr_netflow = 0
    queue = 0
    Area = total_lambda + netflow
    #print(lambdat2)
    sl = (2 * (Area - lambdat2*(t3 - t2))) / (pow(t3,2) - pow(t2,2))
    #print(sl)
    for k in np.arange(0, (int((t3)/10)-int(t2/10))+1):
        y = sl*k + lambdat2
        # print(y)
        total_mu += y
        curr_netflow = y - lambda_arr[k + int(t2/10)]
        queue += curr_netflow
        #print(queue)
    #print("error: " + str(queue - netflow))

    return sl

# find t0, t3 for every day
def findt0t3(array, cuttoff):
    t0dist = []
    t3dist = []
    if(max(array) <= cuttoff):
        return 0,0
    for i in np.arange(int(len(array)/2)):
        t0dist.append(abs(array[i] - cuttoff))
    for i in np.arange(int(len(array)/2),len(array)):
        t3dist.append(abs(array[i] - cuttoff))

    t0 = t0dist.index(min(t0dist)) * 10
    t3 = (t3dist.index(min(t3dist)) + int(len(array)/2)) * 10

    return t0,t3

# determine magnitude of temperature increase
def mag_temp_inc(maxtemp, cutoff):
    # mti = magnitude of temperature increase
    tempdiff = maxtemp - cutoff 
    mti = (maxtemp - cutoff) / maxtemp
    #print(mti)
    tempdiff_arr.append(tempdiff)
    g_mtis.append(mti)

# Export data to 2 csvs
# 1) Sub-mesoscale
# 2) Mesoscale
def ExportData(type, file):
    if(type == 'PAQ'):
        #print('PAQ')
        list_of_tuples = list(zip(year_num_arr, day_num_arr,g_Queues,g_Lambdas,g_Mus))
        pd.DataFrame(list_of_tuples, columns=['Year','Day', 'Simulated Queue', 'Lambda', 'Mu' ]).to_csv('ExportedData/Phoenix/2019_PAQ/PAQ ' + str(file) + '.csv')
    if(type == 'QVDF'):
        list_of_tuples = list(zip(g_max_temp_arr, g_avg_temp_arr,g_ps,D_arr,C_arr,DC_arr,g_mtis,avg_mu_arr,muOC_arr))    
        pd.DataFrame(list_of_tuples, columns=['Max Temperature', 'Avg Temperature', 'P', 'D', 'C','D/C','MTI','mu','mu/C']).to_csv('ExportedData/Phoenix/2019_QVDF/QVDF ' + str(file) + '.csv')


def clearArrs():
    g_Queues.clear()
    g_Lambdas.clear()
    g_Mus.clear()
    g_Mus_eq.clear()
    g_ps.clear()
    g_avg_temp_arr.clear()
    g_max_temp_arr.clear()
    tempdiff_arr.clear()
    g_mtis.clear()
    avg_lambda.clear()
    DC_arr.clear()
    D_arr.clear()
    C_arr.clear()
    avg_mu_arr.clear()
    muOC_arr.clear()
    mu_diff.clear()
    year_num_arr.clear()

def parallel_func(data,fileNames):
    return QueueBasedTemperatureModel(data,fileNames)
    
'''

PARRALEL PROCESSING: REQUIRE MULTIPLE PROCESSES, GOOD FOR SUPER COMPUTER USAGE
Description: 12-core runtime = 591 seconds for 10,111 data points, 625,600 lines each, producing 2 csv files (1 with 13,400 lines, the other with 93)

'''
if __name__ == '__main__':
    start_time = time.perf_counter()
    Area = pd.read_csv('Area.csv')
    chunksize = 2500
    for i in range(int(10111/chunksize)+1):
        data = []
        fileNames = []
        k = 0
        for root, dirs, files in os.walk('datasets/CleanedData/2019/'):
            for file in files:
                if file.endswith('.csv'):    
                    if(dataset_num % chunksize != 0 or dataset_num == 0):
                        if(k >= dataset_num):
                            index = Area.loc[Area['File Name'] == file].index[0]
                            #if(Area.iloc[int(index)]['Yes'] == 1):
                            data.append(pd.read_csv('datasets/CleanedData/2019/' + str(file)))
                            fileNames.append(str(file))
                            #print(dataset_num)
                            print('finished ' + file)
                            dataset_num += 1
                    k+=1
        pool = mp.Pool(processes=13)
        pool.starmap(parallel_func, zip(data, fileNames))

        pool.close()
        pool.join()
        data.clear()
        dataset_num += 1
    
    
    
    
'''

SERIAL PROCESSING: FAST FOR EASY TO COMPUTE TASKS WHICH DO NOT REQUIRE MULTI CORE PROCESSING

'''
'''if __name__ == "__main__":

    Area = pd.read_csv('Area.csv')

    fileNames = []
    x_value = [day_arr,day_arr]
    for root, dirs, files in os.walk('datasets/CleanedData/2019/'):
        for file in files:
            if file.endswith('.csv'):    
                if(dataset_num >= 0):
                    index = Area.loc[Area['File Name'] == file].index[0]
                    if(Area.iloc[int(index)]['Yes'] == 1):
                        data = (pd.read_csv('datasets/CleanedData/2019/' + str(file)))
                        findcutoff(data)
                    #QueueBasedTemperatureModel(pd.read_csv('datasets/CleanedData/2019/' + str(file)),10)
                    #fileNames.append('datasets/CleanedData/2019/' + str(file))
                    print(dataset_num)
                    #print('finished ' + file)
                    #ExportData('PAQ', file)
                    #ExportData('QVDF', file)
                    #clearArrs()
                    dataset_num += 1
    print(g_temp_arr)
    sorted_arr = np.sort(g_temp_arr)[::-1]

    # calculate the index corresponding to the top 97.5% of the elements
    index_975 = int(np.ceil(len(sorted_arr) * 0.025))

    # select the top 97.5% of the elements
    top_975 = sorted_arr[:index_975]
    print(np.max(top_975))'''


