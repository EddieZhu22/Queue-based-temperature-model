import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from shapely.geometry import Point, shape
import os


#df = pd.read_csv('ExportedData/Overview.csv')
df = pd.read_csv('ExportedData/Overview.csv')
fig = px.scatter_mapbox(df, lat="Lat", lon="Long", hover_name="id", hover_data=["Max Temperature","P", "D/C","D","C","MTI","mu","mu/C"],color="P",
                        #size="D/C",
                        opacity = 0.9,
                        color_continuous_scale = px.colors.sequential.Redor, zoom=3)
fig.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
      ])
#fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
fig.write_html("ExportedData/TemperaturePhoenix.html")
#fig.write_image("ExportedData/fig1.png")

'''fig = go.Figure(data=go.Scattergeo(
    lat = df['Lat'],
    lon = df['Long'],
    text = df['P'].astype(str),
    marker = dict(
        color = df['P'],
        colorscale = px.colors.sequential.Redor,
        opacity = 0.7,
        size = 10,
        colorbar = dict(
            titleside = "right",
            outlinecolor = "rgba(68, 68, 68, 0)",
            ticks = "outside",
            showticksuffix = "last",
            dtick = 0.1
        )
    )
))'''

#fig.update_layout(mapbox_style="open-street-map")
#fig.show()


