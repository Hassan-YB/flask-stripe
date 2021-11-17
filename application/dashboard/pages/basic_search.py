import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import dash_table
#from app import app
from application import appDashboard
from application.dashboard.utils import spinner



def create_layout(appDashboard):
    return dbc.Container(
                         [
                         spinner,
                         dbc.Row(
                                 [

                                 dbc.Col(
                                         [
                                          dbc.FormGroup(
                                                        [
                                                        dbc.Label("Security Basic Search:"),
                                                        dbc.Input(id="search-text",placeholder="Search here", type="text"),
                                                        ]
                                          )

                                         ],width={"size": 6, "offset": 3}
                                 ),
                                 dbc.Col(
                                         [
                                         dbc.Button("Search", id="search-submit",color="secondary", className="mr-1", n_clicks=0, style={'margin-top':'35px'})
                                         ]
                                 )

                                 ]
                         ),
                         dbc.Row(
                                 [
                                 dbc.Col(id = "table-s-col",
                                         children=[
                                         dash_table.DataTable(
                                                id='table-s',
                                                style_data_conditional=[
                                                               {
                                                                   'if': {'row_index': 'odd'},
                                                                   'backgroundColor': '#eaebeb'
                                                               }
                                                ],

                                                style_header={
                                                          'backgroundColor': '#c2c3c5',
                                                           'fontWeight': 'bold',
                                                           'fontSize': 20
                                                },
                                                style_cell={'font-family':'BrandonGrotesqueRegular','whiteSpace': 'pre-line','fontSize':16}

                                                )
                                         ],style = {'visibility':'hidden'}
                                 )
                                 ],style = {'margin-bottom':'30px'}
                         ),
                         dbc.Row(
                                 [
                                 dbc.Col(id = "table-d-col",
                                         children=[
                                         dash_table.DataTable(
                                                id='table-d',
                                                style_data_conditional=[
                                                               {
                                                                   'if': {'row_index': 'odd'},
                                                                   'backgroundColor': '#eaebeb'
                                                               }
                                                ],

                                                style_header={
                                                          'backgroundColor': '#c2c3c5',
                                                           'fontWeight': 'bold',
                                                           'fontSize': 20
                                                },
                                                style_cell={'font-family':'BrandonGrotesqueRegular','whiteSpace': 'pre-line','fontSize': 16}
                                                )
                                         ],style = {'visibility':'hidden'}
                                 ),
                                 dbc.Col(id = "graph-col",
                                         children=[
                                         dcc.Graph(id="graph-h")
                                         ],style = {'visibility':'hidden'}
                                 )
                                 ]
                         )

                         ],fluid=True
        )
