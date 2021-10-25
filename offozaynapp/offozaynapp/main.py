
import tools
import plotly_tools
import streamlit as st
import pandas as pd
import numpy as np
import platform
import maptools

st.set_page_config(page_title="Offshore Leaks Exploration")


st.title('Offshore Leaks')

#st.write(platform.platform())

select_list = ['', 'jurisdiction', 'countries', 'country_codes', 'continents', 'company_type', 'jurisdiction_description', 'table']
select_dict = {k.replace('_', ' ').title(): k for k in select_list}


select_key = st.sidebar.selectbox(
    "Which field would you like to explore?",
    tuple(select_dict.keys())
)


select_link = st.sidebar.selectbox(
    "Which link type would you like to explore?",
    ('','registered address','related entity','shareholder of','intermediary of','trust settlor of','protector of',
 'joint settlor of','beneficiary of','tax advisor of','beneficial owner of','resident director of','secretary of','director of','trustee of trust of',
 'successor protector of','alternate director of','investment advisor of','authorised person / signatory of',
 'assistant secretary of','officer of','auditor of','legal advisor of','general accountant of',
 'Nominee Shareholder of','co-trustee of trust of','register of shareholder of','reserve director of','register of director of','bank signatory of',
 'personal directorship of','stockbroker of','correspondent addr. of','appointor of', 'president of',
 'treasurer of','safekeeping of','Nominee Director of','vice president of','Nominee Protector of','nominated person of',
 'auth. representative of','custodian of','chairman of','records & registers of',
 'Nominee Investment Advisor of','Nominee Trust Settlor of','Nominee Beneficiary of','Nominee Beneficial Owner of','nominee name of')
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
    lat_lon_data = tools.load_lat_lon()
    st.subheader('Raw data')
    st.write(lat_lon_data.head())
    st.map(lat_lon_data, zoom=1)
    
    
# if st.checkbox('Show plotly'):
#     plotly_tools.test_plotly()


if st.checkbox('Show Map plotly'):
    if select_link=='':
        st.write('Please select a link!')
    if select_link:
        maptools.map_plotly(select_link)
