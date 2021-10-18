
import streamlit as st
import pandas as pd
import numpy as np

st.title('Offshore Leaks')


DATA_LAT_LON = ('https://drive.google.com/file/d/10l-06L2waxvG6pKbCwuX1wtPtrPjgPO4/view?usp=sharing')

JURISDICTION_DATA_URL = ('https://drive.google.com/file/d/10eXidO511doY2M7dLQMZE00lGSVu_Vez/view?usp=sharing')

# Taken with modification from
# https://newbedev.com/pandas-how-to-read-csv-file-from-google-drive-public"""
get_url = lambda u: 'https://drive.google.com/uc?export=download&id=' + u.split('/')[-2]
    
    

@st.cache
def load_data(url, nrows):
    data = pd.read_csv(get_url(url), nrows=nrows) 
    return data


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(JURISDICTION_DATA_URL, 10000)
# Notify the reader that the data was successfully loaded.
# data_load_state.text('Loading data...done!')
data_load_state.text("Done! (using st.cache)")

data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
lat_lon_data = load_data(DATA_LAT_LON, 10000)
# Notify the reader that the data was successfully loaded.
# data_load_state.text('Loading data...done!')
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data.head())
    st.subheader('Jurisdiction Source')
    hist_values = data['jurisdiction_source'].value_counts().sort_values()
    st.bar_chart(hist_values)
    
if st.checkbox('Show Latitude & Longitude data'):
    st.subheader('Raw data')
    st.write(lat_lon_data.head())
    st.map(lat_lon_data)
