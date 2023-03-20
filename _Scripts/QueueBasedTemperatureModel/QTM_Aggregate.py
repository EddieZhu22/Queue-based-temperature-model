import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import sys
import os
import math
import statistics
import warnings
from matplotlib.colors import LinearSegmentedColormap
import mpl_scatter_density # adds projection='scatter_density'

sys.path.append('/_Scripts')
c = []
takenpoints = [] 
avg_MaxTemp = []
avg_AvgTemp = []
avg_p = [] 
avg_d = [] 
avg_dc = [] 
avg_mti = [] 
avg_mu = []
avg_dmu = []
avg_muc = [] 
id = []

est_p_arr= [] 
p_arr= [] 
C_arr= [] 
D_arr= [] 
DC_arr= [] 
mti_arr= []
mu_arr= [] 
muc_arr= []
df1 = pd.read_csv('LatitudeLongitude.csv')
print(df1['Long'].values[1])



def averages(dataframe):
    dataframe = dataframe.replace(0, np.nan)

    # remove all rows with NaN values
    dataframe = dataframe.dropna()
    avg_MaxTemp.append(dataframe["Max Temperature"].mean())
    avg_AvgTemp.append(dataframe["Avg Temperature"].mean())
    avg_p.append(dataframe["P"].mean())
    avg_d.append(dataframe["D"].mean())
    c.append(max(df['C']))
    avg_dc.append(dataframe["D/C"].mean())
    avg_mti.append(dataframe["MTI"].mean())
    avg_mu.append(dataframe['Mu Equation'].mean())
    avg_dmu.append((dataframe["D"]/dataframe['Mu Equation']).mean())
    avg_muc.append(dataframe["mu/C"].mean())

# 10km * 10km
def situationalanalysis(dataframe):
    for i in range(len(dataframe)):
        print(i)
        if (i not in takenpoints):
            global points
            points = []
            C_arr = []
            Lat = round(dataframe['Lat'].values[i], 2)
            Lon = round(dataframe['Long'].values[i],2)
            for i in range(5):
                for i in range(5):
                    Lon = round(Lon,2)
                    Lat = round(Lat,2)
                    C_arr.append(findpoint(Lat,Lon))
                    #print(Lat, Lon)
                    Lon += 0.02
                Lat-=0.02    
                Lon = dataframe['Long'].values[i]
            #print(C_arr)
            filtered_items = filter(lambda item: item is not None, C_arr)
            C_arr= list(filtered_items)
            final_C = max(C_arr)
           # print(points)
            for l in range (len(points)):
                c[points[l]] = final_C
                avg_muc[points[l]] = avg_mu[points[l]]/final_C
                avg_dc[points[l]] = avg_d[points[l]]/final_C
                df = pd.read_csv('ExportedData/2019_QVDF/' + 'QVDF GriddedDataSetPoint' + str(id[points[l]]) + '_2019.csv.csv')
                
                final_C_arr = np.full(len(df['C'].to_list()), final_C)
                df['C'] = final_C_arr
                print(final_C)
                for i in range(len(df['C'].tolist())):
                    df['D/C'][i] = df['D'][i]/df['C'][i]
                    df['mu/C'][i] = df['mu'][i]/df['C'][i]
                    #print(df['mu/C'][i])
                    #print(df['D/C'][i])
                df.to_csv('ExportedData/2019_QVDF/' + 'QVDF GriddedDataSetPoint' + str(id[points[l]]) + '_2019.csv.csv')

                
def findpoint(lat,lon):
    for i in range(len(df1["Lat"])):
        if(round(df1['Lat'].values[i],2) == lat):
            if(df1['Long'].values[i] == lon):
                if(i not in takenpoints):
                    #print("yes")
                    takenpoints.append(i)
                    points.append(i)
                    return float(c[i])
                    
                    
def add_est_P(df):
    # set arrays
    LnPs = []
    LnD_Cs = []
    #Calculate LN (Ps, D/Cs)
    warnings.filterwarnings("ignore", message="divide by zero encountered in log")
    for i in range(len(df['P'])):
        if(np.log(df['D/C'][i]) != float('-inf') and df['P'][i] > 0):
            LnPs.append(np.log(df['P'][i]))
            LnD_Cs.append(np.log(df['D/C'][i]))

    LnD_Cs1 = np.array(LnD_Cs).reshape(-1, 1)

    # If Ln Dcs, Ln Ps
    if(len(LnD_Cs) > 0 and len(LnPs) > 0):
        fd_n = LinearRegression().fit(LnD_Cs1, np.array(LnPs))
        r_sq = fd_n.score(LnD_Cs1, LnPs)
        
        n = fd_n.coef_[0]
        fd = math.exp(fd_n.intercept_)
        #  Add Est_P
        for i in range(len(df['P'])):
            #print(np.log(df['D/C'][i]))
            if(np.log(df['D/C'][i]) != float('-inf') and df['P'][i] > 0):
                est_p = fd * pow((df['D/C'][i]),n)
                est_p_arr.append(est_p)
                p_arr.append(df['P'][i])
                C_arr.append(df['C'][i])
                DC_arr.append(df['D/C'][i])
                D_arr.append(df['D'][i])
                mti_arr.append(df['MTI'][i])
                mu_arr.append(df['mu'][i])
                muc_arr.append(df['mu/C'][i])
i = 0
Lat = []
Lon = []
avg_est_p_arr = []
for root, dirs, files in os.walk('ExportedData/Phoenix/2019_QVDF/'):
        for file in files:
            if file.endswith('.csv'):    
                #print('started ' + str(file))
                df = pd.read_csv('ExportedData/Phoenix/2019_QVDF/' + file)
                add_est_P(df)
                avg_est_p_arr.append(np.mean(est_p_arr))
                   # print(est_p_arr)
                #df.to_csv('ExportedData/2019_QVDF/' + file, index=False)
                #pd.concat([df, pd.DataFrame(est_p_arr, columns=['est P'])], axis = 1).to_csv('ExportedData/2019_QVDF/' + file)
                averages(df)
                #findTop975(df)
                #PAQ GriddedDataSetPoint1201095_2019.csv
                id.append(file[24:31])
                #print(file[5:40])
                index = df1.loc[df1['FileName'] == file[5:40]].index[0]
                Lat.append(round(df1.iloc[int(index)]['Lat'], 2))
                Lon.append(round(df1.iloc[int(index)]['Long'], 2))
                #print(id)
                print('finished ' + str(file))
                est_p_arr.clear()
                i += 1
#df = pd.read_csv('ExportedData/P_Model_Validation.csv')
           
'''white_viridis = LinearSegmentedColormap.from_list('white_viridis', [
    (0, '#ffffff'),
    (1e-20, '#440053'),
    (0.2, '#404388'),
    (0.4, '#2a788e'),
    (0.6, '#21a784'),
    (0.8, '#78d151'),
    (1, '#fde624'),
], N=256)

def using_mpl_scatter_density(fig, x, y):
    ax = fig.add_subplot(1, 1, 1, projection='scatter_density')
    density = ax.scatter_density(x, y, cmap=white_viridis, dpi = 25)
    fig.colorbar(density, label='Number of points per pixel')

fig = plt.figure()
using_mpl_scatter_density(fig, df['P'], df['Est P'])
plt.show()
fig.savefig('PvsEstP.png')'''
#situationalanalysis(df1)


#list_of_tuples = list(zip(p_arr,est_p_arr,D_arr,C_arr,DC_arr,mti_arr,mu_arr,muc_arr))    
#pd.DataFrame(list_of_tuples, columns=['P', 'Est P', 'D', 'C', 'D/C', 'MTI', 'mu', 'mu/C']).to_csv('ExportedData/P_Model_Validation.csv')
print(Lat)
#list_of_tuples = list(zip(id,avg_MaxTemp, avg_AvgTemp, avg_p, avg_d,c,avg_dc,avg_mti,avg_mu,avg_muc))    
#pd.concat([df1, pd.DataFrame(list_of_tuples, columns=['id', 'Max Temperature', 'Avg Temperature' 'P', 'D', 'C','D/C','MTI','mu', 'mu/C'])], axis=1).to_csv('ExportedData/Overview.csv')
list_of_tuples = list(zip(Lat,Lon,id,avg_MaxTemp, avg_AvgTemp, avg_p, avg_est_p_arr, avg_d,c,avg_dc,avg_mti,avg_mu,avg_dmu ,avg_muc))                    
pd.DataFrame(list_of_tuples, columns=['Lat', 'Long', 'id', 'Max Temperature', 'Avg Temperature', 'P', 'Est P', 'D', 'C','D/C','MTI','mu','D/mu', 'mu/C']).to_csv('ExportedData/Overview2.csv')