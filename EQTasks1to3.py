import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

data_sample = pd.read_csv('data\\DataSample.csv')

#######Cleanup##########

print(f'Size of data before cleaning {len(data_sample)}')

#removing duplicates having identical TimeSt and geo location
data_sample.drop_duplicates(subset =['Latitude','Longitude',' TimeSt'], keep = False, inplace = True)

print(f'Size of data after cleaning {len(data_sample)}')

##########Label#######################
poi_list = pd.read_csv('data\\POIList.csv')

distinct_pois = []
for ind in poi_list.index:
    distinct_pois.append(poi_list['POIID'][ind])
      
def calculateDistance(x1,y1,x2,y2):  
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
    return dist  

labelled_data = []

for index in data_sample.index:
    x1=data_sample['Latitude'][index]
    y1=data_sample['Longitude'][index]
    min_distance = -1
    nearest_poi = 'None'
    for ind in poi_list.index:
        x2=poi_list[' Latitude'][ind]
        y2=poi_list['Longitude'][ind]
        cur_dist = calculateDistance(x1,y1,x2,y2)
        if min_distance == -1 or min_distance > cur_dist:
            min_distance  = cur_dist
            nearest_poi=poi_list['POIID'][ind]
    labelled_data.append([x1,y1,nearest_poi,min_distance])

cols = ['Latitude', 'Longitude', 'POI', 'MinDist']

labelled_df = pd.DataFrame(labelled_data, columns=cols)

###########Analysis#########################################

sum_of_dist = {} #dictionary to contain sum of all distances for each poi

for ind in labelled_df.index:
    for poi in distinct_pois:
        if poi == labelled_df['POI'][ind]:
            if poi in sum_of_dist.keys():
                sum_of_dist[poi] = sum_of_dist[poi] + labelled_df['MinDist'][ind]
            else:
                sum_of_dist[poi] = labelled_df['MinDist'][ind]      
    

def calculateMean(sum_of_dist,poi):
    if len(labelled_df[(labelled_df['POI'] == poi)]) == 0:
        return 0
    else:
        return sum_of_dist[poi] / len(labelled_df[(labelled_df['POI'] == poi)])

def calculateStandardDeviation(sum_dev,poi):
    if len(labelled_df[(labelled_df['POI'] == poi)]) == 0:
        return 0
    else:
        return sum_dev[poi] / len(labelled_df[(labelled_df['POI'] == poi)])

mean_of_poi = {}
for poi in distinct_pois:
    mean_of_poi[poi] =  calculateMean(sum_of_dist,poi)
    print(f'Mean for {poi} is {mean_of_poi[poi]}')
 
 
standard_dev_sum_poi = {}

for ind in labelled_df.index:
    for poi in distinct_pois:
        if poi == labelled_df['POI'][ind]:
            if poi in standard_dev_sum_poi.keys():
                standard_dev_sum_poi[poi] = standard_dev_sum_poi[poi] + (mean_of_poi[poi] - labelled_df['MinDist'][ind])**2
            else:
                standard_dev_sum_poi[poi] = (mean_of_poi[poi] - labelled_df['MinDist'][ind])**2         

sd_of_poi = {}
for poi in distinct_pois:
    sd_of_poi[poi] =   calculateStandardDeviation(standard_dev_sum_poi,poi)
    print(f'Standard deviation for {poi} is {sd_of_poi[poi]}')

x_centre_poi = {}
y_centre_poi = {}
x_axis_points_poi = {}
y_axis_points_poi = {}


for poi in distinct_pois:
    x_centre_poi[poi] = 0
    y_centre_poi[poi] = 0
    x_axis_points_poi[poi] = labelled_df[(labelled_df['POI'] == poi)]['Latitude']
    y_axis_points_poi[poi] = labelled_df[(labelled_df['POI'] == poi)]['Longitude']

for ind in poi_list.index:
    for poi in distinct_pois:
        if poi_list['POIID'][ind] == poi:
            x_centre_poi[poi] = poi_list[' Latitude'][ind]
            y_centre_poi[poi] = poi_list['Longitude'][ind]

def computeRadius(points_x,points_y,center_x,center_y):
    r = np.sqrt((points_x - center_x)**2 + (points_y - center_y)**2)
    t = 100 # percent
    r0 = np.percentile(r, t)
    return r0
    
circle_colors = ['r','b','y','g']
dot = '.'
circle_poi = []
counter = 0
for poi in distinct_pois:
    if not len(x_axis_points_poi[poi]) == 0:
        plt.plot(x_axis_points_poi[poi], y_axis_points_poi[poi], circle_colors[counter] + dot)
        radius = computeRadius(x_axis_points_poi[poi],y_axis_points_poi[poi],x_centre_poi[poi], y_centre_poi[poi])
        circle_poi.append(plt.Circle((x_centre_poi[poi], y_centre_poi[poi]), radius, color=circle_colors[counter], fill=False))
        plt.gca().add_artist(circle_poi[counter])
        counter += 1
        density = len(x_axis_points_poi[poi]) / ( 3.14 * radius * radius)
        print(f'The radius of circle for {poi} is {radius} with density {density}')

plt.axis([-200, 250, -275,150])
plt.show()
