import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import dash_bootstrap_components as dbc
from app import app
import numpy as np
import plotly.graph_objs as go

nav_menu = dbc.Nav(
    [
        dbc.NavLink("Home ", active=True, href="/"),
        dbc.NavLink("Page 2", href="/apps/app1"),
        
    ]
)

dft = pd.read_csv('./timesData.csv')
dft2 = dft[dft["year"]==2016][0:50]
dft2.research = pd.to_numeric(dft2.research, errors="coerce")
dft2.world_rank  = pd.to_numeric(dft2.world_rank, errors="coerce")
TirParGroup = dft2.groupby('university_name')
# ParGroup = dftableau.groupby('country')
y1=TirParGroup['research'].agg(np.mean).sort_values(ascending=False)
y2=TirParGroup['world_rank'].agg(np.mean)



trace1 = {
  'x': y1.index.get_level_values(0).tolist(),
                
  'y': y1,
  'name': 'Research',
  'type': 'bar'
}
trace2 = {
  'x':  y1.index.get_level_values(0).tolist(),
                
  'y': y2,
  'name': 'World Rank',
  'type': 'bar'
}
data = [trace1, trace2]

layout_graph = {
  'xaxis': {'title': 'Pays'},
  'barmode': 'relative',
  'title': 'Correlation'
}
fig = go.Figure(data = data, layout = layout_graph)

def generate_table(dataframe, max_rows=50):
    return html.Table(style={
        'color':colors2['text'],
        'height':'27vh'
    }, children=[
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])
colors2 ={
    'background':'#1EC1EB',
    'text':'#000000'
}

layout = html.Div([
    html.Br(),
    nav_menu,
    html.Br(),
    html.Br(),
    html.H3(style={'text-align': 'center'} , children=["Les 50 meilleurs universités de l'année 2016"]),
    html.Br(),
    html.Section(style={'display':'flex'}, children=[


    html.Div([
     html.Br(),
     html.Br(),
    #  html.H3(style={'text-align': 'center'} , children=["Analyse de corrélation"]),
     html.Br(),
     dcc.Graph(
        
        figure=fig
    ),
    ]),
  
    
     html.Br(),
    ]),
   
                    
         html.Article(style={'width':'49vw',}, children=[

        dash_table.DataTable(
        export_format='csv',
        data=dft2.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in dft2.columns],
        page_size=25,  # we have less data in this example, so setting to 20
    
        fixed_rows={'headers': True},
        style_table={'height': '50vh', 'overflowY': 'auto', 'width':'50vw', 'margin-left':'1vw'},
        style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color':'white'},
        style_cell={
            'backgroundColor': 'white',
            'color': 'black'
        },),

    html.Br(),
    ]),    
    
  
])
