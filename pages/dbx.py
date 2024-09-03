from dash import dcc,html
from components.header import header_layout
from components.inputs import inputLayout




dbx = html.Div([
    dcc.Location(id= 'url', refresh=False),
    html.Div(id= 'page-content', children =[
    html.Div(id ='calculator',children= [
    inputLayout ,

    # html.Div(id="tables" ,children=[DatabricksCalcDashTable])
    html.Div(id = "Outputs", children= [
        html.H3(id ="table-message"),
        html.Table(id = "total_cost_table" )
    ])
    ])
    ])

])
