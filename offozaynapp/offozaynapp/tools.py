
import config
import streamlit as st
import graphviz as graphviz
import pandas as pd
import networkx as nx
from PIL import Image

# Taken with modification from
# https://newbedev.com/pandas-how-to-read-csv-file-from-google-drive-public"""
get_url = lambda u: 'https://drive.google.com/uc?export=download&id=' + u.split('/')[-2]
    
    
@st.cache
def load_data(url, nrows):
    data = pd.read_csv(get_url(url), nrows=nrows) 
    return data

@st.cache
def load_lat_lon(nrows):
#     return pd.read_csv(get_url(config.sheet_url), nrows=nrows) 
    return pd.read_csv('./data/nodes_lat_lon.csv', nrows=nrows) 


@st.cache(suppress_st_warning=True)
def read_xlsx(sheet, nrows=10000):
    #return pd.read_excel(get_url(config.sheet_url), sheet_name=sheet, nrows=nrows)
    return pd.read_excel('./data/specific_edges.xlsx', sheet_name=sheet, nrows=nrows)


def create_digraph_new(df, count=10):   
    """
    https://discuss.streamlit.io/t/support-for-networkx-pyvis-and-folium/190/2
    """
    final_count = min(df.shape[0], count)
    df.sort_values(by='weight', ascending=False, inplace=True)
    G = nx.DiGraph()
    G.add_weighted_edges_from([tuple(x) for x in df.head(final_count).values])
    dot = nx.nx_pydot.to_pydot(G)
    st.graphviz_chart(dot.to_string())
    
def show_image(name, caption):
    image = Image.open(f'images/{name}')
    st.image(image, caption=caption)

    
