from dash.dependencies import Input, Output, State
from dash import dash_table
import pandas as pd
import numpy as np
import json
import re
import requests
from datetime import datetime
import dash
#from app import app
from application import appDashboard
import plotly.graph_objects as go
from flask_login import  current_user, login_fresh, logout_user



@appDashboard.callback(
        [Output("table-s","data"),
         Output("table-s","columns"),
         Output("loading-output","style"),
         Output("table-s-col","style"),
         Output('table-d', 'data'),
         Output('table-d','columns'),
         Output('graph-h','figure'),
         Output('table-d-col','style'),
         Output('graph-col','style')],
        [Input("search-submit","n_clicks"),
         Input('table-s', 'active_cell')],
        [State("search-text","value"),
         State("loading-output","style"),
         State("table-s-col","style"),
         State('table-s','data'),
         State('table-d-col','style'),
         State('graph-col','style')]
)

def update_table(n1,active_cell,search_value,style_loading,col_style,data_s,table_col_style,graph_col_style):
    button_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    global data
    global columns
    if login_fresh() == False:logout_user()
    if current_user.is_authenticated == True:
        apikey= current_user.apikey
    else: return    
    if button_id == "search-submit":
        style_loading = {'visibility':'visible'}
        
        res = requests.get("https://tepiloradata.com/T-Api/S/"+search_value.strip()+"/Json?apikey="+apikey) #9bb87e4c-5613-401c-a618-2e4374f87e00")
        res = res.json()
        df = pd.DataFrame.from_dict(pd.json_normalize(res[1:]), orient='columns')
        columns=[{"name": i, "id": i} for i in df.columns]
        data=df.to_dict('records')
        col_style = {'visibility':'visible','margin-left':'30px','margin-right':'30px','height':'500px','overflow':'scroll','overflow-x': 'hidden'}
        table_col_style = {'visibility':'hidden'}
        graph_col_style = {'visibility':'hidden'}
        return [data,columns,style_loading,col_style,[],[],{},table_col_style,graph_col_style]
    if active_cell:
        df_s = pd.DataFrame.from_dict(pd.json_normalize(data_s), orient='columns')

        row_number = active_cell['row']

        code = df_s['TepiloraCode'][row_number]

        link_graph = "https://tepiloradata.com/T-Api/H/0/"+code+"/Json?apikey=" +apikey #"9bb87e4c-5613-401c-a618-2e4374f87e00"


        res_graph = requests.get(link_graph)

        res_graph = res_graph.json()

        columns_values = res_graph[0]['H']

        columns_h = columns_values[0]

        data_values = res_graph[0]['H']

        data_h = np.array(data_values[1:])

        df_h = pd.DataFrame(data=data_h,columns=columns_h)

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=df_h['Time'],
                                 y=df_h['Price'],
                                 mode='lines',
                                 marker_color="#343a40")
        )

        fig.update_layout(
                paper_bgcolor='#ffffff',
                plot_bgcolor='#ffffff',
                font=dict(color='#999c9f')
        )


        link_table_d = "https://tepiloradata.com/T-Api/D/"+code+"/Json?apikey=" + apikey #"9bb87e4c-5613-401c-a618-2e4374f87e00"

        res_table = requests.get(link_table_d)

        res_table = res_table.json()

        df_table = pd.DataFrame.from_dict(pd.json_normalize(res_table[0]['Data']), orient='columns')


        df_table.drop(columns=['Benchmark'],axis=1,inplace=True)


        df_table_1 = pd.DataFrame.from_dict(pd.json_normalize(res_table[0]['Data']['Benchmark'][0]), orient='columns')

        df_table_1.rename(columns={'Name': 'Benchmark-Name', 'Weight': 'Benchmark-Weight'}, inplace=True)

        df_d = pd.concat([df_table_1,df_table],axis=1)

        df_d = df_d.T

        df_d['Label'] = df_d.index

        df_d['Values'] = df_d[0]


        df_d.reset_index(drop=True, inplace=True)
        df_d.drop(columns=[0],axis=1,inplace=True)


        columns_d=[{"name": i, "id": i} for i in df_d.columns]
        data_d=df_d.to_dict('records')

        table_col_style = {'visibility':'visible','margin-left':'30px','margin-right':'30px','height':'500px','overflow':'scroll','overflow-x': 'hidden'}
        graph_col_style = {'visibility':'visible'}

        return [data,columns,style_loading,col_style,data_d,columns_d,fig,table_col_style,graph_col_style]


    else:
        graph_col_style = {'visibility':'hidden'}
        return [[],[],{},{},[],[],{},{},graph_col_style]
