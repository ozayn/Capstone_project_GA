
import tools
import networkx as nx
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

@st.cache(suppress_st_warning=True, show_spinner=False)
def get_graph():
    data_load_state = st.text('Loading data ... ')
    nodes = tools.load_nodes()
    edges = tools.load_edges()
    edges = edges.sample(500)
    data_load_state.text('Loading data ... done!')
    
    col_edges_conv = {'START_ID': 'source', 
                  'END_ID': 'target',
                  'link': 'Type',
                  'active_days': 'Active Days'
                  }
    col_nodes_conv = {'countries': 'Country', 
                    'continents': 'Region',
                    'jurisdiction': 'Jurisdiction', 
                    'service_provider': 'Service Provider',
                    'company_type': 'Company Type'}

    edges_cols = ['START_ID', 'END_ID', 'active_days', 'link']
    nodes_cols = ['node_id', 'countries', 'continents','jurisdiction', 'service_provider', 'company_type', 'location']
    linkData = edges[edges_cols].rename(columns = col_edges_conv)
    nodeData = nodes[nodes_cols].rename(columns = col_nodes_conv )
    data_load_state = st.text('Making graph ...')
    G = nx.from_pandas_edgelist(linkData, 'source', 'target', True, nx.DiGraph())
    nx.set_node_attributes(G, nodeData.set_index('node_id').to_dict('index'))
    data_load_state.text('Making Graph ... done!')
    return G


@st.cache(suppress_st_warning=True, show_spinner=False)
def test_plotly():

    G = get_graph()

    field = 'location'
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = eval(G.nodes[edge[0]][field])
        x1, y1 = eval(G.nodes[edge[1]][field])
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
        



    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = eval(G.nodes[node][field])
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text



    fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='Title',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
#                 margin=dict(b=20,l=5,r=5,t=40),
#                 annotations=[ dict(
#                     text="",
#                     showarrow=False,
#                     xref="paper", yref="paper",
#                     x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

    st.plotly_chart(fig)
    
def test_plotly2():


    G = nx.random_geometric_graph(200, 0.125)

#     data_load_state = st.text('Loading data...')
#     nodes = tools.load_nodes()
#     edges = tools.load_edges()
#     data_load_state.text('Loading data...done!')
    
    
#     st.write(nodes.head(2))
#     st.write(edges.head(2))
    
#     G = get_graph(nodes, edges)

    field = 'pos'
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]][field]
        x1, y1 = G.nodes[edge[1]][field]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node][field]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text



    fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='Title',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
#                 margin=dict(b=20,l=5,r=5,t=40),
#                 annotations=[ dict(
#                     text="",
#                     showarrow=False,
#                     xref="paper", yref="paper",
#                     x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

    st.plotly_chart(fig)
    
def sample_plotly():


    # Add histogram data
    x1 = np.random.randn(200) - 2
    x2 = np.random.randn(200)
    x3 = np.random.randn(200) + 2

    # Group data together
    hist_data = [x1, x2, x3]

    group_labels = ['Group 1', 'Group 2', 'Group 3']

    # Create distplot with custom bin_size
    fig = ff.create_distplot(
             hist_data, group_labels, bin_size=[.1, .25, .5])

    # Plot!
    st.plotly_chart(fig, use_container_width=True)
