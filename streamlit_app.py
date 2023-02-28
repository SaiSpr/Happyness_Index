    
# import statements
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import date
from io import StringIO
import plotly.express as px
import seaborn as sns


df = pd.read_csv("df_final.csv")

# adding title and text in the app

st.sidebar.title("World Happiness Report:")

country_list = ["All","Western Europe", "South Asia", "Southeast Asia", "East Asia", "North America and ANZ","Middle East and North Africa", "Latin America and Caribbean","Central and Eastern Europe","Commonwealth of Independent States","Sub-Saharan Africa"] 
select = st.sidebar.selectbox('Filter the region here:', country_list, key='1')

if select =="All":
    filtered_df = df
else:   
    filtered_df = df[df['Region']==select]

score = st.sidebar.slider('Select min Happiness Score', min_value=0, max_value=10, value = 2) # Getting the input.
df = df[df['Happiness_Score'] <= score] # Filtering the dataframe.



st.image("world-happiness-report.jpg", caption='World Happiness Report')

#print dataframe
st.write(filtered_df)

fig = px.scatter(filtered_df,
                x="Economy",
                y="Health",
                size="Happiness_Score",
                color="Region",
                hover_name="Country",
                size_max=10)
st.write(fig)

st.write(px.bar(filtered_df, y='Happiness_Score', x='Country'))

#correlate data
corr = filtered_df.corr()

#using matplotlib to define the size

plt.figure(figsize=(8, 8))

#creating the heatmap with seaborn

fig1 = plt.figure()
ax = sns.heatmap(
    corr, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True
)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
);
st.pyplot(fig1)






from geopy.geocoders import Nominatim

# Load the data
df_geo = pd.read_csv('df_final_geo.csv')

# Create the map
fig = px.scatter_mapbox(df_geo, lat='Latitude', lon='Longitude', hover_name='Country', hover_data=['Happiness.Rank', 'Happiness.Score'], color='Happiness.Score', size='Economy..GDP.per.Capita.', zoom=1, height=500)
fig.update_layout(mapbox_style='carto-positron')

# Build the Streamlit app
st.title('Happiness Index 2017 Map')
st.plotly_chart(fig)


#new map
df = pd.read_csv('df_final_geo.csv')

import folium
from folium.plugins import MarkerCluster

# Create a map centered on the world
map_happiness = folium.Map(location=[0, 0], zoom_start=2)

# Add a marker cluster to the map
marker_cluster = MarkerCluster().add_to(map_happiness)

# Add a marker for each country in the dataframe
for i in range(len(df)):
    lat = df.loc[i, 'latitude']
    lon = df.loc[i, 'longitude']
    country = df.loc[i, 'Country name']
    score = df.loc[i, 'Ladder score']
    popup_text = f'{country}<br>Score: {score}'
    folium.Marker(location=[lat, lon], popup=popup_text).add_to(marker_cluster)

# Display the map
st.write(map_happiness._repr_html_(), unsafe_allow_html=True)


