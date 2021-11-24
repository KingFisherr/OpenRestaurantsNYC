###################################
###################################

import pandas as pd 
import numpy as np 
import folium 

def addallmarkers(df, map):
    tooltip = "Click Here For More Info"

    for a,b, c in zip(df.Latitude, df.Longitude, df['Restaurant Name']): 
        marker = folium.Marker(location=[a, b], popup="<stong>" + c +"</stong>",tooltip = tooltip)
        marker.add_to(map)
    #m.save('map.html')

df = pd.read_csv(r"C:\Users\Tahsin Provath\Desktop\Hunter - Fall 2021\CS 39542\Project files\Open_Restaurant_Applications.csv")
newdf = df.dropna()

m = folium.Map(location=[40.724971, -74.004477], zoom_start=12)
addallmarkers(newdf, m)
# # marker = folium.Marker(
# #     location=[40.724971, -74.004477],
# #     popup="<stong>HERE ARTS CENTER</stong>",
# #     tooltip=tooltip)
# # marker.add_to(m)
m.save('map.html')