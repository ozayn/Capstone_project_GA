
import tools
import streamlit as st
import pandas as pd
import numpy as np
import platform

st.set_page_config(page_title="Offshore Leaks Exploration")


st.title('Offshore Leaks')

#st.write(platform.platform())

select_list = ['', 'jurisdiction', 'countries', 'country_codes', 'continents', 'company_type', 'jurisdiction_description', 'table']
select_dict = {k.replace('_', ' ').title(): k for k in select_list}


select_key = st.sidebar.selectbox(
    "Which field would you like to explore?",
    tuple(select_dict.keys())
)

select_value = select_dict[select_key]

if select_value:
    st.write(select_value)
    
    if tools.is_local():
        if select_value == 'countries':
            tools.show_image('top_25_countries__address__intermediary__officer__entity.png', 'Countries')



    weight_data = tools.read_xlsx(select_value)
    st.write(f'Total {weight_data.shape[0]} edges')

    st.subheader('Edges - Weighted')
    st.write(weight_data.head())

#     weight_data = weight_data[weight_data['weight']>1]
    
    if st.checkbox('Show raw data'):
        st.subheader(f'{select_key} Source')
        hist_values = weight_data[f'{select_value}_source'].value_counts().sort_values(ascending=False)
        n_columns = st.slider('How many columns?', 0, hist_values.shape[0], min(10, hist_values.shape[0]))
        st.bar_chart(hist_values.head(n_columns))
        st.write(hist_values)

    
    n_edges = st.slider('How many edges?', 0, min(weight_data.shape[0], 100), min(10, weight_data.shape[0]))
    tools.create_digraph_new(weight_data, n_edges)
    
if st.checkbox('Show Latitude & Longitude data'):
    lat_lon_data = tools.load_lat_lon(10000)
    st.subheader('Raw data')
    st.write(lat_lon_data.head())
    st.map(lat_lon_data, zoom=1)
