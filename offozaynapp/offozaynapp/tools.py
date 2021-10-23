
import config
import streamlit as st
import graphviz as graphviz
import pandas as pd
import networkx as nx
from PIL import Image
import platform
import plotly.figure_factory as ff
import numpy as np

# Taken with modification from
# https://newbedev.com/pandas-how-to-read-csv-file-from-google-drive-public"""
get_url = lambda u: 'https://drive.google.com/uc?export=download&id=' + u.split('/')[-2]
    

def check_platform():
    pl = platform.platform()
    if pl.startswith('macOS'):
        return 'local'
    return 'remote'

def is_local():
    return check_platform()=='local'
    
    
@st.cache(suppress_st_warning=True, show_spinner=False)
def load_data(url, nrows):
    data = pd.read_csv(get_url(url), nrows=nrows) 
    return data

@st.cache(suppress_st_warning=True, show_spinner=False)
def load_nodes():
    if is_local():
        return pd.read_csv('./data/nodes_single.csv', low_memory=False) 
    else:
        return pd.read_csv(get_url(config.nodes), low_memory=False)
    
@st.cache(suppress_st_warning=True, show_spinner=False)
def load_edges():
    if is_local():
        return pd.read_csv('./data/edges_all_single.csv', low_memory=False) 
    else:
        return pd.read_csv(get_url(config.edges), low_memory=False)

@st.cache
def load_lat_lon(nrows, show_spinner=False):
    if is_local():
        return pd.read_csv('./data/nodes_lat_lon.csv', nrows=nrows) 
    else:
        return pd.read_csv(get_url(config.lat_lon_url), nrows=nrows)


@st.cache(suppress_st_warning=True, show_spinner=False)
def read_xlsx(sheet, nrows=10000):
    if is_local():
        return pd.read_excel('./data/specific_edges_single.xlsx', sheet_name=sheet, nrows=nrows)
    else:
        return pd.read_excel(get_url(config.sheet_url), sheet_name=sheet, nrows=nrows)


def create_digraph_new(df, count=10):   
    """
    https://discuss.streamlit.io/t/support-for-networkx-pyvis-and-folium/190/2
    """
    final_count = min(df.shape[0], count)
    df.sort_values(by='weight', ascending=False, inplace=True)
    G = nx.DiGraph()
    G.add_weighted_edges_from([tuple(x) for x in df.head(final_count).values])
    dot = nx.nx_pydot.to_pydot(G)
    st.graphviz_chart(dot.to_string(), use_container_width=True)
    
def show_image(name, caption):
    image = Image.open(f'images/{name}')
    st.image(image, caption=caption)

    
