# layout of app
from dash import html, dcc
from .header import header_layout
from .inputs import inputLayout
from pages.dbx import dbx

layout = html.Div([
    header_layout,
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Databricks', value='tab-1',
                selected_style={'color': 'white', 'fontWeight': 'bold', 'background-color': '#8451EC'}),
        dcc.Tab(label='Snowflake', value='tab-2',
                selected_style={'color': 'white', 'fontWeight': 'bold', 'background-color': '#8451EC'}),
        dcc.Tab(label="AKS", value="tab-3",
                selected_style={'color': 'white', 'fontWeight': 'bold', 'background-color': '#8451EC'})
    ]),
    html.Div(id='tabs-content')
])
