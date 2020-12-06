import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import dash_bootstrap_components as dbc
from app import app
import numpy as np
import plotly.graph_objs as go
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.figure_factory as ff



dft = pd.read_csv('./timesData.csv')
nb_data = 50
n_comp = 8


dfs = dft[dft.year==2016].iloc[:nb_data,:]
dfs = dfs.dropna()
dfs.world_rank = [each.replace('=','') for each in dfs.world_rank]
# dfs.world_rank = pd.to_numeric(dft.world_rank, errors='coerce')
# dfs.income = pd.to_numeric(dft.income, errors='coerce')
# dfs.international = pd.to_numeric(dft.international, errors='coerce')
# dfs.total_score = pd.to_numeric(dft.total_score, errors='coerce')
# dfs.num_students = [str(each).replace(',','') for each in dft.num_students]
# dfs.international_students = [each.replace('%','') for each in dft.international_students]
# dfs.female_male_ratio = [str(each).split() for each in dft.female_male_ratio]
# dfs.female_male_ratio = [round((float(each[0]) / float(each[2])),2)*100 for each in dft.female_male_ratio]
# dfs.female_male_ratio = pd.to_numeric(dft.female_male_ratio, errors='coerce')


dfs.research = pd.to_numeric(dft.research, errors="coerce")
dfs.world_rank  = pd.to_numeric(dft.world_rank, errors="coerce")
TirParGroup = dfs.groupby('university_name')
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
  'xaxis': {'title': 'Université'},
  'barmode': 'relative',
  'title': 'Correlation',
  
}
fig = go.Figure( data = data, layout = layout_graph)
fig.update_layout(
    plot_bgcolor='#181B1E' ,
    paper_bgcolor='#181B1E',
    font_color='#DCDCDC',
    
    
)

markdown_text = '''
* Réaliser une veille sur la librairie Dash.
* Faire une analyse du jeu de données correspondant au classement des 50 meilleures universités en 2016.
* Réaliser une Analyse en Composantes Principales (vous pourrez vous appuyer sur la librairie Scikit-Learn) https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
* Mettre en place un Dashbord Dash multi-pages permettant de répondre à la question initiale : De toutes les universités du monde, quelles sont les meilleures ? La première page de votre Dashbord mettra en évidence l'analyse des données des 50 meilleures universités de l'année 2016 (avant L'ACP).

#### 1ère page

* Dans cette première page se trouvera notamment une table des données des 50 meilleurs universités de l'année 2016 avec un bouton de téléchargement permettant de télécharger un tableau .csv des données.
* Plusieurs graphiques mettant en évidences des corrélations entre certains critères (par exemple : qualité de la recherche en fonction du rand mondial du classement des universités etc..)
#### 2eme page

Cette page permettra d'afficher les résultats issus de l'ACP. On pourra ainsi y trouver des graphiques ainsi que des paragraphes de textes mettant en évidence des variables explicatives (par exemple la valeur propre, la proportion, le cumulé, les composantes principales (CP), les scores, les distances).

Vous mettrez en ligne votre Dashboard Dash sur le serveur Cloud Heroku

'''

modal = html.Div(
    [
        dbc.Button(style={'margin-bottom':'5vh','margin-left':'2vw','backgroundColor':'#181B1E'}, children=["Détail du brief"], id="open-xl"),
        dbc.Modal(
            [
                dbc.ModalHeader(""),
                dbc.ModalBody(style={}, children=[
                    html.H5(style={'text-align': 'center',}, children=['Contexte du projet']),
                    html.H5(style={'text-align': 'center',}, children=['Classement des universités']),
                    html.P(style={}, children=[
                        "Le classement des universités est une pratique difficile, politique et controversée. Il existe des centaines de systèmes de classement universitaires nationaux et internationaux différents, dont beaucoup sont en désaccord les uns avec les autres.Le Times Higher Education World University Ranking est largement considéré comme l'une des mesures universitaires les plus influentes et les plus largement observées. Fondée au Royaume-Uni en 2010, elle a été critiquée pour sa commercialisation et pour avoir 'affaibli' les établissements non anglophones. " 
                    ]),
                    html.H5(style={'text-align': 'center',}, children=['Analyse en Composantes Principales']),
                    html.P(style={}, children=[
                        " Pour vous aider dans votre analyse du jeux de données, vous réaliserez une Analyse en Composantes Principales.Cette analyse permettra de répondre à certaines questions du type : quelles ressemblances peut-il y avoir d'une université à une autre. Quelles ressemblances existent-il entre différents critères d'évaluation des universités ? Vous pourrez ainsi définir quand est-ce que 2 universités se ressemblent et quand est-ce qu'elles se ressemblent du point de vue de l'ensemble des colonnes (c'est-à-dire des critères d'évaluation du Times Higher Education World University Ranking).Est-il possible de faire un bilan des ressemblances ? ( Vous chercherez ici à faire une typologie, une partition des universités, c'est-à-dire à construire des groupes d'universités homogènes du point de vue de l'ensemble des variables. A l'intérieur d'un groupe, les individus se ressemblent et d'un groupe à l'autre ils sont différents."
                    ]),
                    html.H5(style={'text-align': 'center',}, children=['Analyse en Composantes Principales']),
                    html.P(style={}, children=[
                        dcc.Markdown(children=markdown_text),
                       
                    ]),


                ]),
                dbc.ModalFooter(
                    dbc.Button(style={'backgroundColor':'#181B1E'},children=["Fermer"], id="close-xl", className="ml-auto")
                ),
            ],
            id="modal-xl",
            size="xl",
        ),
    ]
)



# Modal 2 Corrélation
colonnes = ['world_rank', 'total_score', 'research', 'teaching', ]
data_pca = dfs[colonnes]
lay1_fig2 = ff.create_scatterplotmatrix(data_pca, diag='histogram',
                                  colormap='Viridis',
                                  colormap_type='cat',
                                  height=500, width=1000)


nav_menu = dbc.Nav(
    [
        dbc.NavLink(style={'color':'#DCDCDC'},children=["Home "], active=True, href="/"),
        dbc.NavLink(style={'color':'#DCDCDC'},children=["Page 2"], href="/acp"),
        
    ]
)


layout = html.Div(style={'backgroundColor':'#212529', 'padding-top':'2vh', 'padding-botton':'4vh'}, children=[
  
  nav_menu,

  html.H1(style={'text-align': 'center', 'color':'#DCDCDC', 'margin-top':'2vh', 'margin-bottom':'3vh'} , children=[ "Dashboard"]),
  html.Section(style={'height':'70vh', 'display':'flex', 'justify-content':'space-around'}, children=[
      html.Article(style={ 'backgroundColor':'#181B1E', 'height':'70vh','width':'66vw', 'padding-top':'1.2vh','border-radius':'15px'}, children=[
           dcc.Graph(
        
        figure=fig
    ),
      ]),
      html.Article(style={'backgroundColor':'#212529', 'height':'70vh', 'width':'30vw'}, children=[
        html.Div(style={'backgroundColor':'#181B1E', 'height':'33vh', 'width':'30vw','border-radius':'15px'}, children=[]),
        html.Div(style={'backgroundColor':'#181B1E', 'margin-top':'4vh','height':'33vh', 'width':'30vw','border-radius':'15px'}, children=[])
      ]),
  ]

  ),
  html.H2(style={'text-align': 'center','color':'#DCDCDC', 'margin-top':'5vh','margin-bottom':'5vh'},children=["Les 50 meilleurs universités de l'année 2016 "]),
  html.Section(style={'display':'flex', 'margin-bottom':'5vh','justify-content':'space-around'},children=[
      html.Article(style={'backgroundColor':'#181B1E', 'height':'75vh','width':'25vw','border-radius':'15px'},children=[]),
      html.Article(style={'backgroundColor':'#181B1E','margin-left':'2vw', 'height':'75vh', 'width':'70vw','border-radius':'15px'},children=[
          
          dash_table.DataTable(
            id='table',
          export_format='csv',
            columns=[{"name": i, "id": i} for i in dfs.columns],
            data=dfs.to_dict('records'),
            page_size=15,
            style_table={'height': '71vh', 'overflowY': 'auto', 'width':'69vw'},
                
            style_header={'backgroundColor': '#151819', 'color':'white'},
            style_cell={
                'backgroundColor': '#1C1F23',
                'color': '#DCDCDC'
            },),
    

      ])
  ]),
  html.Br(),
  html.Br(),
  html.Section([
      
  ]),
  modal,
  
   
])

def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

app.callback(
    Output("modal-xl", "is_open"),
    [Input("open-xl", "n_clicks"), Input("close-xl", "n_clicks")],
    [State("modal-xl", "is_open")],
)(toggle_modal)
