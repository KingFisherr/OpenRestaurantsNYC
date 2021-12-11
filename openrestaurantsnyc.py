#Title: Tahsin Provath
#Email: tahsin.provath58@myhunter.cuny.edu
#Resources: Pandas, numpy, folium, matplotlib, and branca
#URL: https://kingfisherr.github.io/OpenRestaurantsNYC/

import pandas as pd 
import numpy as np 
import folium 
import matplotlib.pyplot as plt
import re
import branca

# Adds legend for each outdoor dining options to assist in visuals on folium
def add_categorical_legend(folium_map, title, colors, labels):
    if len(colors) != len(labels):
        raise ValueError("colors and labels must have the same length.")

    color_by_label = dict(zip(labels, colors))
    
    legend_categories = ""     
    for label, color in color_by_label.items():
        legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"
        
    legend_html = f"""
    <div id='maplegend' class='maplegend'>
      <div class='legend-title'>{title}</div>
      <div class='legend-scale'>
        <ul class='legend-labels'>
        {legend_categories}
        </ul>
      </div>
    </div>
    """
    script = f"""
        <script type="text/javascript">
        var oneTimeExecution = (function() {{
                    var executed = false;
                    return function() {{
                        if (!executed) {{
                             var checkExist = setInterval(function() {{
                                       if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                          clearInterval(checkExist);
                                          executed = true;
                                       }}
                                    }}, 100);
                        }}
                    }};
                }})();
        oneTimeExecution()
        </script>
      """
   

    css = """

    <style type='text/css'>
      .maplegend {
        z-index:9999;
        float:right;
        background-color: rgba(255, 255, 255, 1);
        border-radius: 5px;
        border: 2px solid #bbb;
        padding: 10px;
        font-size:12px;
        positon: relative;
      }
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 0px solid #ccc;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    """

    folium_map.get_root().header.add_child(folium.Element(script + css))

    return folium_map

# Adds relevant information to restaurant markers (i.e. name, address)
def addallmarkers(df, map, zipc):
    if (zipc > 0):
      map = folium.Map(location=[ df['Latitude'].iloc[0], df['Longitude'].iloc[0]], zoom_start=16)
    tooltip = "Click Here For More Info"
    for a,b,c,d, e in zip(df.Latitude, df.Longitude, df['Restaurant Name'], df['Seating Interest (Sidewalk/Roadway/Both)'], df['Business Address']): 
        if a > 0:
            if d == 'both':
                html = "<h5><b>" + c + "</h5></b>" + '<p style="font-family:Courier; color:Black; font-size: 12px;">' + e + "</p>"
                iframe = folium.IFrame(html,width=125,height=100)
                marker = folium.Marker(location=[a, b], popup= folium.Popup(iframe, min_width= 125), tooltip = tooltip, icon = folium.Icon(color = 'red', icon= 'cutlery', prefix= 'fa'))
                marker.add_to(map)
            if d == 'sidewalk':
                html = "<h5><b>" + c + "</h5></b>" + '<p style="font-family:Courier; color:Black; font-size: 12px;">' + e + "</p>"
                iframe = folium.IFrame(html,width=125,height=100)              
                marker = folium.Marker(location=[a, b], popup= folium.Popup(iframe, min_width= 125), tooltip = tooltip, icon = folium.Icon(color = 'blue', icon= 'cutlery', prefix= 'fa'))
                marker.add_to(map)
            if (d == 'roadway' or d == 'openstreets'):
                html = "<h5><b>" + c + "</h5></b>" + '<p style="font-family:Courier; color:Black; font-size: 12px;">' + e + "</p>"
                iframe = folium.IFrame(html,width=125,height=100)              
                marker = folium.Marker(location=[a, b], popup= folium.Popup(iframe, min_width= 125), tooltip = tooltip, icon = folium.Icon(color = 'green', icon= 'cutlery', prefix= 'fa'))
                marker.add_to(map)       
    return map         

# Finds open dining options via zip code
def getzip(df):
  # Takes user input to determine which type of map to generate (see below)
  zipc = int(input("Enter a Zipcode: "))
  # If zipcode is specified
  if (zipc > 0):
    checkdf = df[df['Postcode'] == zipc]
    return checkdf
  # If user wants to see all, drop all NaN rows and plot all markers
  elif (zipc == 0):
    checkdf = df.dropna()
    return checkdf

# Finds open dining options via location name
def getname(df):
  name = input("Enter location name: ")
  df = df.dropna()
  checkdf = df[df['NTA'].str.contains(name)]
  #print (checkdf)
  return checkdf


# Read in data 
df = pd.read_csv(r"C:\Users\Tahsin Provath\Desktop\Hunter - Fall 2021\CS 39542\Project files\Open_Restaurant_Applications.csv")

# Clean NaN values from certain columns
df['Sidewalk Dimensions (Area)'] = df['Sidewalk Dimensions (Area)'].fillna(0)
df['Roadway Dimensions (Area)'] = df['Roadway Dimensions (Area)'].fillna(0)
df['Latitude'] = df['Latitude'].fillna(0)
df['Longitude'] = df['Longitude'].fillna(0)

# New DF for each borough to plot stacked bar chart
boro_df = df[df['Borough'] == 'Manhattan']
numbers_m = boro_df['Seating Interest (Sidewalk/Roadway/Both)'].value_counts()
boro_df = df[df['Borough'] == 'Queens']
numbers_q = boro_df['Seating Interest (Sidewalk/Roadway/Both)'].value_counts()
boro_df = df[df['Borough'] == 'Brooklyn']
numbers_bk = boro_df['Seating Interest (Sidewalk/Roadway/Both)'].value_counts()
boro_df = df[df['Borough'] == 'Bronx']
numbers_bx = boro_df['Seating Interest (Sidewalk/Roadway/Both)'].value_counts()
boro_df = df[df['Borough'] == 'Staten Island']
numbers_si = boro_df['Seating Interest (Sidewalk/Roadway/Both)'].value_counts()

# Generate stacked bar plot
plotdf = pd.DataFrame([['Manhattan', numbers_m[0] + numbers_m[3] , numbers_m[1], numbers_m[2]], ['Queens', numbers_q[0] + numbers_q[3], numbers_q[1], numbers_q[2]], ['Brooklyn', numbers_bk[0] + numbers_bk[3], numbers_bk[1], numbers_bk[2]],  ['Bronx', numbers_bx[0] + numbers_bx[3],numbers_bx[1], numbers_bx[2]],
                   ['Staten Island', numbers_si[0] + numbers_si[3], numbers_si[1], numbers_si[2]]],
                  columns=['Borough', 'Both', 'Sidewalk', 'Roadway'])
  
# plot data in stack manner of bar type
plotdf.plot(x='Borough', kind='bar', stacked=True,
        title='Outdoor Dining Options by Borough')

#plt.show()
plt.savefig("borodata.png", bbox_inches='tight')

# Center Map around Manhattan 
m = folium.Map(location=[40.724971, -74.004477], zoom_start=12)

#Search by zipcode or name
choice = input ("Search by zip or name: ")

if (choice == 'zip'):
  checkdf = getzip(df)
  zipc = 1
elif (choice == 'name'):
  checkdf = getname(df)
  zipc = 2
elif (choice == 'all'):
  zipc = 0
  checkdf = df.dropna()

# Add markers based on user request
m = addallmarkers(checkdf, m, zipc)

# Add legend
m = add_categorical_legend(m, 'Outdoor Dining',
                             colors = ['green','blue', 'red'],
                           labels = ['Roadway Only', 'Sidewalk Only', 'Both'])
if (zipc == 1):
  m.save(r"C:\Users\Tahsin Provath\Desktop\Hunter - Fall 2021\CS 39542\OpenRestaurantsNYC\map.html")
  print ("Done")
elif (zipc == 2):
  m.save(r"C:\Users\Tahsin Provath\Desktop\Hunter - Fall 2021\CS 39542\OpenRestaurantsNYC\smap.html")
  print ("Done")
elif (zipc == 0):
  m.save(r"C:\Users\Tahsin Provath\Desktop\Hunter - Fall 2021\CS 39542\OpenRestaurantsNYC\fmap.html")
  print ("Done")
