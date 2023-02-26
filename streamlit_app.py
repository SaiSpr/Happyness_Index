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
        df_happy = df.sort_values(by='Ladder score', ascending=False).head(10)
        st.write('Top 10 Happiest Countries')
        st.table(df_happy)

    # Show the top 10 unhappiest countries
    elif selection == 'Top 10 Unhappiest Countries':
        df_unhappy = df.sort_values(by='Ladder score').head(10)
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
fig = px.scatter(df_filtered, x='Logged GDP per capita', y='Ladder score', color='Regional indicator', size='Population',
                 hover_name='Country name', title=f'Happiness Index ({year})')
st.plotly_chart(fig)

# Add radio buttons to choose a variable to plot against the ladder score
variable = st.sidebar.radio('Select a variable', ['Logged GDP per capita', 'Social support', 'Healthy life expectancy', 'Freedom to make life choices'])

# Create a scatter plot
fig = px.scatter(df_filtered, x=variable, y='Ladder score', color='Regional indicator', size='Population',
                 hover_name='Country name', title=f'Happiness Index ({year})')
st.plotly_chart(fig)

# Add a date range selector to filter the data by date
start_date = st.sidebar.date_input('Start date', min_value=df['Date'].min(), max_value=df['Date'].max())
end_date = st.sidebar.date_input('End date', min_value=df['Date'].min(), max_value=df['Date'].max(), value=df['Date'].max())

# Filter the dataframe by date range
df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]


# Add a color picker to change the color scheme of the visualization
color_scheme = st.sidebar.color_picker('Select a color', value='#1f77b4')

# Create a scatter plot with the selected color scheme
fig = px.scatter(df_filtered, x='Logged GDP per capita', y='Ladder score', color='Regional indicator', size='Population',
                 hover_name='Country name', title=f'Happiness Index ({year})', color_discrete_sequence=[color_scheme])
st.plotly_chart(fig)

# Add a selectbox to choose a data column to display
column = st.sidebar.selectbox('Select a column', df.columns)

# Display a table with the selected column
st.write(df_filtered[[column]])

# Add a checkbox group to choose countries to compare
countries = st.sidebar.checkbox('Select countries to compare', options=df_filtered['Country name'].unique())

# Display a line chart comparing the selected countries
if countries:
    fig = px.line(df_filtered[df_filtered['Country name'].isin(countries)], x='year', y='Ladder score', color='Country name',
                  title=f'Happiness Index ({year}) - Comparison')
    st.plotly_chart(fig)
    
# Add a file uploader to upload a new data file
file = st.sidebar.file_uploader('Upload a data file', type=['csv'])

# Load the new data file and display a summary
if file:
    new_df = pd.read_csv(file)
    st.write(new_df.describe())
