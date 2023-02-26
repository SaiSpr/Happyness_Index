import streamlit as st
import pandas as pd
import plotly.express as px

df_2015 = pd.read_csv('2015.csv')
df_2016 = pd.read_csv('2016.csv')
df_2017 = pd.read_csv('2017.csv')
df_2018 = pd.read_csv('2018.csv')
df_2019 = pd.read_csv('2019.csv')

df = pd.read_csv('df_final.csv')

def app():
    st.title('World Happiness Index Data')
    st.sidebar.title('Explore')

    # Add a selectbox to the sidebar
    options = ['Top 10 Happiest Countries', 'Top 10 Unhappiest Countries', 'Correlation Analysis']
    selection = st.sidebar.selectbox('Select an option', options)

    # Show the top 10 happiest countries
    if selection == 'Top 10 Happiest Countries':
        df_happy = df.sort_values(by='Happiness_Score', ascending=False).head(10)
        st.write('Top 10 Happiest Countries')
        st.table(df_happy)

    # Show the top 10 unhappiest countries
    elif selection == 'Top 10 Unhappiest Countries':
        df_unhappy = df.sort_values(by='Happiness_Score').head(10)
        st.write('Top 10 Unhappiest Countries')
        st.table(df_unhappy)

    # Show correlation analysis
    elif selection == 'Correlation Analysis':
        st.write('Correlation Analysis')
        corr = df.corr()
        fig = px.imshow(corr)
        st.plotly_chart(fig)
       
       
# Add a slider to filter the data by year
year = st.sidebar.slider('Select a year', min_value=2015, max_value=2019, value=2019)

# Filter the dataframe by year
df_filtered = df[df['Year'] == year]


# Add a checkbox to select multiple regions
regions = st.sidebar.multiselect('Select regions', options=df['Region'].unique())

# Filter the dataframe by regions
df_filtered = df[df['Region'].isin(regions)]


# Add a dropdown to select a specific country
country = st.sidebar.selectbox('Select a country', options=df['Country'].unique())

# Filter the dataframe by country
df_filtered = df[df['Country'] == country]


# Add a scatter plot to visualize the relationship between GDP per capita and Ladder score
fig = px.scatter(df_filtered, x='Economy', y='Health', color='Region', size = 'Happiness_Score'
                 hover_name='Country', title=f'Happiness Index ({year})')
st.plotly_chart(fig)

# Add radio buttons to choose a variable to plot against the ladder score
variable = st.sidebar.radio('Select a variable', ['Economy', 'Family', 'Health', 'Freedom'])

# Create a scatter plot
fig = px.scatter(df_filtered, x='Family', y='Freedom', color='Region', size='Happiness_Score', hover_name='Country', title=f'Happiness Index ({year})')

st.plotly_chart(fig)

# # Add a date range selector to filter the data by date
# start_date = st.sidebar.date_input('Start date', min_value=df['Date'].min(), max_value=df['Date'].max())
# end_date = st.sidebar.date_input('End date', min_value=df['Date'].min(), max_value=df['Date'].max(), value=df['Date'].max())

# # Filter the dataframe by date range
# df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]


# Add a color picker to change the color scheme of the visualization
color_scheme = st.sidebar.color_picker('Select a color', value='#1f77b4')

# Create a scatter plot with the selected color scheme
fig = px.scatter(df_filtered, x='Economy', y='Trust', color='Region', size='Happiness_Score',
                 hover_name='Country', title=f'Happiness Index ({year})', color_discrete_sequence=[color_scheme])
st.plotly_chart(fig)

# Add a selectbox to choose a data column to display
column = st.sidebar.selectbox('Select a column', df.columns)

# Display a table with the selected column
st.write(df_filtered[[column]])

# Add a checkbox group to choose countries to compare
countries = st.sidebar.checkbox('Select countries to compare', options=df_filtered['Country'].unique())

# Display a line chart comparing the selected countries
if countries:
    fig = px.line(df_filtered[df_filtered['Country'].isin(countries)], x='Year', y='Happyness_Score', color='Country',
                  title=f'Happiness Index ({year}) - Comparison')
    st.plotly_chart(fig)
    
# Add a file uploader to upload a new data file
file = st.sidebar.file_uploader('Upload a data file', type=['csv'])

# Load the new data file and display a summary
if file:
    new_df = pd.read_csv(file)
    st.write(new_df.describe())
    
    
    
    
# # import statements
# import streamlit as st
# import numpy as np
# import pandas as pd
# import altair as alt
# import matplotlib.pyplot as plt
# from datetime import datetime
# from datetime import date
# from io import StringIO
# import plotly.express as px
# import seaborn as sns


# df = pd.read_csv("df_final.csv")

# # adding title and text in the app

# st.sidebar.title("World Happiness Index 2021:")

# country_list = ["All","Western Europe", "South Asia", "Southeast Asia", "East Asia", "North America and ANZ","Middle East and North Africa", "Latin America and Caribbean","Central and Eastern Europe","Commonwealth of Independent States","Sub-Saharan Africa"] 
# select = st.sidebar.selectbox('Filter the region here:', country_list, key='1')

# if select =="All":
#     filtered_df = df
# else:   
#     filtered_df = df[df['Region']==select]

# score = st.sidebar.slider('Select min Happiness Score', min_value=5, max_value=10, value = 10) # Getting the input.
# df = df[df['Happiness_Score'] <= score] # Filtering the dataframe.



# st.image("https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.hyderabaddccb.org%2Fworld-happiness-index%2F&psig=AOvVaw3nMcPUvX2Yy_VvUm3Afd_u&ust=1677532026305000&source=images&cd=vfe&ved=2ahUKEwimtr71i7T9AhXlQ2wGHVqEBvgQjRx6BAgAEAo", caption='World Happiness Report')

# #print dataframe
# st.write(filtered_df)

# fig = px.scatter(filtered_df,
#                 x="Economy",
#                 y="Health",
#                 size="Happiness_Score",
#                 color="Region",
#                 hover_name="Country",
#                 size_max=10)
# st.write(fig)

# st.write(px.bar(filtered_df, y='Happiness_Score', x='Country'))

# #correlate data
# corr = filtered_df.corr()

# #using matplotlib to define the size

# plt.figure(figsize=(8, 8))

# #creating the heatmap with seaborn

# fig1 = plt.figure()
# ax = sns.heatmap(
#     corr, 
#     vmin=-1, vmax=1, center=0,
#     cmap=sns.diverging_palette(20, 220, n=200),
#     square=True
# )
# ax.set_xticklabels(
#     ax.get_xticklabels(),
#     rotation=45,
#     horizontalalignment='right'
# );
# st.pyplot(fig1)
