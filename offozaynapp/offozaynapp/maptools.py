# https://plotly.com/python/lines-on-maps/

import streamlit as st

import plotly.graph_objects as go
import pandas as pd
import tools

@st.cache(suppress_st_warning=True, show_spinner=False)
def map_plotly(select_value=None):

    data_load_state = st.text('Loading data ... ')
    nodes = tools.load_nodes()
    edges = tools.load_edges()
    if select_value:
        edges = edges[edges['link']==select_value]
    st.write(edges.head(2))
    data_load_state.text('Loading data ... done!')


    fig = go.Figure()

    fig.add_trace(go.Scattergeo(
        locationmode = 'country names',
        lon = nodes['longitude'].tolist(),
        lat = nodes['latitude'].tolist(),
        hoverinfo = 'text',
        text = nodes['countries'].tolist(),
        mode = 'markers',
        marker = dict(
            size = 2,
            color = 'rgb(255, 0, 0)',
            line = dict(
                width = 3,
                color = 'rgba(68, 68, 68, 0)'
            )
        )))

    flight_paths = []
    for i in range(edges.shape[0]):
        fig.add_trace(
            go.Scattergeo(
                locationmode = 'country names',
                lon = [edges.iloc[i]['longitude_source'], edges.iloc[i]['longitude_target']],
                lat = [edges.iloc[i]['latitude_source'], edges.iloc[i]['latitude_target']],
                mode = 'lines',
                line = dict(width = 1,color = 'blue'),
#                 opacity = float(df_flight_paths['cnt'][i]) / float(df_flight_paths['cnt'].max()),
            )
        )

    fig.update_layout(
        title_text = '',
        showlegend = False,
        geo = dict(
            scope = 'world',
            projection_type = 'equirectangular',
            showland = True,
            landcolor = 'rgb(243, 243, 243)',
            countrycolor = 'rgb(204, 204, 204)',
        ),
    )


    st.plotly_chart(fig, use_container_width=True)
