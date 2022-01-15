#----------------------------# Load Your Dependencies#--------------------------#

import dash
from dash import  dcc    # Dash core Components
from dash import html   # HTML for Layout and Fonts
import plotly.express as px           # Plotly Graphs uses graph objects internally
import plotly.graph_objects as go     # Plotly Graph  more customized 
import pandas as pd                   # Pandas For Data Wrangling
from dash import Input, Output  # Input, Output for  Call back functions

#--------------------------#Instanitiate Your App#--------------------------#

app = dash.Dash(__name__) 
app.title = 'Analytics Dashboard'
server = app.server

#--------------------------# Pandas Section #------------------------------#

df =pd.read_csv('Churn_Modelling.csv') 
df['Age_']=pd.cut(df['Age'],3 , labels= ["Young","Mid_Aged","Old"])
df['Balance_']=pd.cut(df['Balance'],3 , labels= ["Low","Mid_Balance","High"])

app.layout = html.Div([
                    html.Div([html.A([html.H2('Analysis Dashboard'),html.Img(src='/assets/analysis.png')],  # A for hyper links
                                        href='http://projectnitrous.com/')],className="banner"),
                    html.Div([dcc.Dropdown(
                        id='corr-dropdown',
                        options=[
                            {'label': 'Tenure', 'value': 'Tenure'},
                            {'label': 'Age', 'value': 'Age'},
                            {'label': 'Balance', 'value': 'Balance'},
                            {'label': 'EstimatedSalary', 'value': 'EstimatedSalary'}
                        ],

                        value=['Tenure', 'Age','Balance'],
                        multi=True,

                    )],className="five columns"),

                    
                    html.Div([
                            dcc.Dropdown(
                                id='sunburst-dropdown',
                                options=[
                                    {'label': 'Exited', 'value': 'Exited'},
                                    {'label': 'Age', 'value': 'Age_'},
                                    {'label': 'Balance', 'value': 'Balance_'},
                                    {'label': 'IsActiveMember', 'value': 'IsActiveMember'}
                                ],

                                value=['Exited', 'Age_','Balance_'],
                                multi=True,

                            )],className="five columns"),
                            
                            html.Div([dcc.Graph(id='corr-graph')],className="five columns"),
                            html.Div([dcc.Graph(id='sunburst-graph')],className="five columns" )
                        
])

@app.callback(                            
    Output('sunburst-graph', 'figure'),
    Input('sunburst-dropdown', 'value')
)
def update_output2(value):
    fig = px.sunburst(df, path=value, values='NumOfProducts') # Graph
    fig.update_traces(textinfo="label") 
    return fig



@app.callback(                            
    Output('corr-graph', 'figure'),
    Input('corr-dropdown', 'value'),
)
def update_output(value):
    n=df[value]
    fig=px.imshow(n.corr(),text_auto=True,aspect="auto")

    return fig


app.run_server()
