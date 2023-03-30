# Queue-based Temperature Model
## Table Of Contents
- [Description](#description)
- [Getting Started](#getting-started)
- [Code Structure](#code-structure)
- [References](#references)
- [License](#license)


## Description
This is a repository is for the Queue-based Temperature Model (QTM). Based on fluid queuing theory, this model highlights a simplified version of the world's atmosphere and the relationships between solar radiation and total solar energy to draw several useful inferences about the system's performance, resilience, and adaptability at multiple scales with little runtime and overhead cost.

### Model Overview
The model first takes in solar radiation & temperature data from a data source. Data for a case study done from 2022-2023 used 2019 NSRDB[1] data to attain a modelled 2-meter height and spatially homogeneous gridded dataset usable for the model. 

Then, the model is split into 2 steps:

**QTM STEP 1** - generates general sub-mesoscale system dynamics (Queue, inflow, outflow)

**QTM STEP 2** - turn these sub-mesoscale system dynamics into something meaningful (mesoscale indicators)

A table describing the equations & symbols used in this model are shown below:
![Table](https://github.com/EddieZhu22/Queue-based-temperature-model/blob/master/Images/Picture1.png)

Background Information: The Queue-based Temperature Model (QTM) is inspired by Newell’s fluid queueing model [2] and the Queue Volume Delay Function’s meso-macro framework [3], which offer the theoretical foundation for the model's underlying principles. The QTM consists of a two-step process. In the first step, sub-mesoscale system dynamics present within each day are obtained. In the second step, these dynamics are leveraged to make inferences on the mesoscale level. This allows for the analysis of the system at different levels of fidelity, providing valuable insights into the system's performance, resilience, and adaptability.
Model Framework: In the first step, intraday dynamics of extreme heat are approximated. When the temperature passes through an “extreme heat” cutoff temperature, a queue of energy (Q(t)) starts forming. The queue has two critical components: an inflow and outflow denoted by λ(t) and µ(t) respectively. λ(t) is given by the incoming solar radiation (Global Horizontal Irradiance). µ(t) is the culmination of all factors that release energy out of the system. Because µ(t) is not directly observable, a linear piecewise function is instead used to approximate the behavior. The net flow at a specific time (π(t)) is given by subtracting λ(t) from µ(t). By integrating the net flow, a queue can be calculated. Boundary conditions of the model, t0 and t3, are at the start of the queue and the end of the queue respectively.
In the second step, using the dynamics present in each day and location, several inferences can be made regarding the system. Model outputs include P (heat exposure duration), C (capacity of the system), and D (total inflow demand). Each day these outputs are different, and give a more comprehensive picture of the system’s performance. These indicators can then directly be used in the mesoscale for further analysis.

![image](https://user-images.githubusercontent.com/51139973/228726659-e7ac356c-c3db-49b3-986e-59a898e132b1.png)

In the second step, using the dynamics present in each day and location, several inferences can be made regarding the system. Model outputs include P (heat exposure duration), C (capacity of the system), and D (total inflow demand). Each day these outputs are different, and give a more comprehensive picture of the system’s performance. These indicators can then directly be used in the mesoscale for further analysis.

### QTM STEP 1

#### EQUATIONS: ![image](https://user-images.githubusercontent.com/51139973/228726931-c1b58771-0ab1-4fae-a8c5-4ba51be840c5.png)

#### STEPS: 
INPUT: 10 minute surface solar radiation & 2-meter height air temperature of the summer (93 days) \
STEP 1.1: Determining the cutoff temperature. The cutoff temperature was set to be the top 2.5% of daily mean summertime temperatures, to prune out non extreme heat days. This resulted in a cutoff temperature of 38.02 °C. Then, the boundary conditions t0 and t3 were determined by finding the closest times to the cutoff temperature the Disruption and Recovery phases.
STEP 1.2: Finding t2 at max Q(t). \
STEP 1.3: Calculating µ(t) using solar radiation data as input. \
STEP 1.4: Computing the area between inflow λ(t) and outflow µ(t) to find the Queue. 

#### Figures:
![Slide3](https://user-images.githubusercontent.com/51139973/228727478-ef015823-2987-4d51-a5d4-b7ff793f6451.PNG)

![Slide2](https://user-images.githubusercontent.com/51139973/228727493-60ca5e82-a2b3-46c6-b8b2-5a4ea57502d9.PNG)

![Slide4](https://user-images.githubusercontent.com/51139973/228727503-bf65bb77-7b9e-4f72-9255-ff46be456696.PNG)

### QTM STEP 2
INPUT: Queue, inflow, and outflow of the day (Q(t), λ(t), and µ(t)).
Based on the outputs from QTM Step 1, several system indicators were produced. The indicators and their formulas are listed below:

![image](https://user-images.githubusercontent.com/51139973/228727782-e5027179-c81b-4e41-9866-2a223467edbe.png)

#### Images:
The following are images of the mesoscale results. Interactive results can be accessed here: https://github.com/EddieZhu22/Queue-based-temperature-model/blob/master/Figures/map3.html

![image](https://user-images.githubusercontent.com/51139973/228728102-9e99fd14-4918-4098-b551-35292e4b4d05.png) \
(openstreetmap.org for providing background) \
![image](https://user-images.githubusercontent.com/51139973/228728432-34c1f15b-da77-47ed-b3e1-446d1f8040fe.png)


## Getting Started
1. Clone the repository to your local machine using git clone https://github.com/YOUR_USERNAME/REPO_NAME.git.
2. Navigate to the repository directory using cd REPO_NAME.
3. Install the necessary dependencies using pip install -r requirements.txt. 
4. Add a datasets folder where you keep a path containing 525600 lines with 3 columns: Minute, Temperature, and Solar Radiation. An example dataset is provided for 1 location. 
5. Run the code in Queue-based_Temperature_Model.py, choose either parralel or serial depending on your system preferences.
6. Run the code in QTM_Aggregate.py to get aggregated average sub-mesoscale results.

## Code Structure
The code is split up into folders: Data Collection, QueueBasedTemperatureModel, and spatial regression.


### Data Collection
By default, data is gathered from the National Solar Radiation Database. The code below describes the basic process of doing so. First, enter an API key, email and specifications. Then, the function will take care of the rest by downloading your desired points. Change the desired years depending on the dataset, although the current specifications, only 2019, 2020, and 2021 are available.
```python
def main():
    global input_data 
    input_data = {
        'attributes': 'ghi,air_temperature',
        'interval': '10',
        'to_utc': 'false',
        
        'api_key': API_KEY,
        'email': EMAIL,
    }
    for name in ['2019','2020','2021']:
        print(f"Processing name: {name}")
        global last_index

        for i in range(last_index, len(points)):
            input_data['names'] = [name]
            input_data['location_ids'] = points[i]
            
            print('Making request for point: ' + str(i+1) + ' out of ' + str(len(points)))
                
            if '.csv' in BASE_URL:
                global headers
                headers = {
                    'x-api-key': API_KEY,
                }
                connected = False
                while(connected == False):
                    response = requests.get(BASE_URL, input_data, headers=headers)

                    if response.status_code == 200:
                        data = response.content
                        connected = True
                        #print(data)
                        # Process data as needed
                    else:
                        print("Error:", response.content)
                        time.sleep(1)

                data = pd.read_csv(StringIO(data.decode('utf-8')), sep=",", header=None, low_memory=False,error_bad_lines=False, index_col=False, dtype=object)

                # Note: CSV format is only supported for single point requests
                # Suggest that you might append to a larger data frame
                #print(f'Response data (you should replace this print statement with your processing): {data}')
                # You can use the following code to write it to a file

                data.to_csv('RawData/GriddedDataSetPoint' + str(points[i]) + '_' + str(name) + '.csv' )
                
                time.sleep(1)

            print(f'Processed')
        last_index = 0
```
To prune out non-study area data points, use this following code from Prune_Study_Area.py to remove data not in a specified shapefile: 
```python
for i in range(len(df['Lat'])):
    found = False
    
    #define the specific latitude and longitude to check
    point_to_check = Point(df['Long'][i],df['Lat'][i])

    # if data point is within the speicified boundaries, set found to true
    for k in range(len(boundaries.geometry)):
        if point_to_check.within(boundaries.geometry[k]):
           found = True
    print(i)
    
    # Append to array to see if data point is within boundary
    if(found == False):
        in_area.append(0)
        #print("Lat")
    else:
        plt.scatter(point_to_check.x, point_to_check.y, c='red')
        in_area.append(1)
    FileNames.append(df['FileName'][i])
list_of_tuples = list(zip(FileNames, in_area))

# Create a dataframe of final results  
pd.DataFrame(list_of_tuples,columns=['File Name','In Study Area']).to_csv('Area.csv')
plt.show()
```

### QueueBasedTemperatureModel
There are 3 scripts, however the main one to use is Queue-based_Temperature_Model.py. Start by importing the data you want by creating a folder called Datasets. Store the data in that path. Then, run the data on the cutoff temperature method.
```python
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
```
It takes the 93 days in the summer and finds the top **2.5%** of temperature values.

Then use the 
```python 
def QueueBasedTemperatureModel(data, file, timehorizon = 10)
```
method to run the model. It should produce 2 csv files 1 for the sub-mesoscale results, and the other for the mesoscale.
```python
def ExportData(type, file):
    if(type == 'PAQ'):
        #print('PAQ')
        list_of_tuples = list(zip(year_num_arr, day_num_arr,g_Queues,g_Lambdas,g_Mus))
        pd.DataFrame(list_of_tuples, columns=['Year','Day', 'Simulated Queue', 'Lambda', 'Mu' ]).to_csv('PATH/TO/FOLDER/PAQ ' + str(file) + '.csv')
    if(type == 'QVDF'):
        list_of_tuples = list(zip(g_max_temp_arr, g_avg_temp_arr,g_ps,D_arr,C_arr,DC_arr,g_mtis,avg_mu_arr,muOC_arr))    
        pd.DataFrame(list_of_tuples, columns=['Max Temperature', 'Avg Temperature', 'P', 'D', 'C','D/C','MTI','mu','mu/C']).to_csv('PATH/TO/FOLDER/QVDF ' + str(file) + '.csv')
```
Lastly, to aggregate the results, QTM_Aggregate.py will take the average of all the results and store it in a csv called Overview.csv.
```python
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
```

### Spatial Regression

Spatial Regression was mostly handled in jupyter notebooks.
The first script, CreatePolygons.ipynb creates an overlapping grid of land cover densities.
Then, in DataVisualization.ipynb, data visualization inclduing regression coefficients were calculated.

## Acknowledgements
Special thanks to Dr. Xuesong Zhou for providing continuous support on this project. Thank you to Dr. Zhi Hua Wang and Dr. Gorgescu for providing feedback and giving very professional and useful tips.
## References
[1] NSRDB https://nsrdb.nrel.gov/ \
[2] Newell, C. (2013). Applications of queueing theory (Vol. 4). Springer Science & Business Media. \
[3] Zhou, X. (2022). A meso-to-macro cross-resolution performance approach for connecting polynomial arrival queue            
           model to volume-delay function with inflow demand-to-capacity ratio. Multimodal Transportation, 1(2). \
           https://doi.org/10.1016/j.multra.2022.100017 

