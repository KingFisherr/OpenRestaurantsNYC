###################################
###################################

import pandas as pd 
import numpy as np 
import folium 
import branca

#use this function to create a custom legend each time we generate a map (maybe for outdoor dining type)
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

# Add photos and add reviews
def addallmarkers(df, map):
    tooltip = "Click Here For More Info"

    for a,b,c, d in zip(df.Latitude, df.Longitude, df['Restaurant Name'], df['Seating Interest (Sidewalk/Roadway/Both)']): 
        if a > 0:
            if d == 'both':
                marker = folium.Marker(location=[a, b], popup="<stong>" + c +"</stong>", tooltip = tooltip, icon = folium.Icon(color = 'red', icon= 'cutlery', prefix= 'fa'))
                marker.add_to(map)
            if d == 'sidewalk':
                marker = folium.Marker(location=[a, b], popup="<stong>" + c +"</stong>", tooltip = tooltip, icon = folium.Icon(color = 'blue', icon= 'cutlery', prefix= 'fa'))
                marker.add_to(map)
            if d == 'roadway':
                marker = folium.Marker(location=[a, b], popup="<stong>" + c +"</stong>", tooltip = tooltip, icon = folium.Icon(color = 'green', icon= 'cutlery', prefix= 'fa'))
                marker.add_to(map)                
# Read in data 
df = pd.read_csv(r"C:\Users\Tahsin Provath\Desktop\Hunter - Fall 2021\CS 39542\Project files\Open_Restaurant_Applications.csv")


df['Sidewalk Dimensions (Area)'] = df['Sidewalk Dimensions (Area)'].fillna(0)
df['Roadway Dimensions (Area)'] = df['Roadway Dimensions (Area)'].fillna(0)
df['Latitude'] = df['Latitude'].fillna(0)
df['Longitude'] = df['Longitude'].fillna(0)


# Drop all NaN rows
#newdf = df.dropna()


# Center Map around Manhattan (might change this)
m = folium.Map(location=[40.724971, -74.004477], zoom_start=12)

zipc = int(input("Enter a Zipcode: "))
checkdf = df[df['Postcode'] == zipc]

addallmarkers(checkdf, m)

m = add_categorical_legend(m, 'Legend',
                             colors = ['green','blue', 'red'],
                           labels = ['Roadway Only', 'Sidewalk Only', 'Both'])


m.save(r"C:\Users\Tahsin Provath\Desktop\Hunter - Fall 2021\CS 39542\OpenRestaurantsNYC\map.html")
print ("Done")