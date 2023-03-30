from shapely.geometry import Point
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import osmnx as ox
import pandas as pd
import matplotlib.pyplot as plt


'''
maricopa_county = gpd.read_file('datasets/MPA/MPA__2019.shp')

point_to_check1 = Point(-112.074,33.448)
maricopa_county = maricopa_county.to_crs({'init': 'epsg:4326'})
maricopa_county.plot()'''
df = pd.read_csv('LatitudeLongitude.csv')

query = {'county': 'Maricopa'}

# get the boundaries of the place (add additional buffer around the query)
boundaries = ox.geocode_to_gdf(query, buffer_dist=5000)
boundaries = boundaries.to_crs('EPSG:4326')


total_not = 0
total_in = 0

in_area = []
FileNames = []

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

