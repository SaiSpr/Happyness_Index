    
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

score = st.sidebar.slider('Select min Happiness Score', min_value=5, max_value=10, value = 10) # Getting the input.
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



import geopy
import folium
from geopy.geocoders import Nominatim

# # Load the World Happiness Index data
data = pd.read_csv("df_final.csv")

# Create a title for the dashboard
st.title("World Happiness Index Map")

# # Create a geolocator object
geolocator = Nominatim(user_agent="streamlit")

# # Create a map centered on the world
m = folium.Map(location=[0, 0], zoom_start=2)

# # Add a marker for each country in the data
for i in data.Country:
#      country = data.loc[i, "Country"]
#      st.title("country")
     location = geolocator.geocode(i)
     if location is not None:
         lat = location.latitude
         lon = location.longitude
         score = data["Happiness_Score"]
         folium.Marker([lat, lon], popup=f"{i}: {score}").add_to(m)
       
import plotly.express as px

fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name='Country', zoom=3)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)

# Display the map
st.write(m._repr_html_(), unsafe_allow_html=True)
