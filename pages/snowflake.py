from dash import dcc, html
from components.snowflakeInputs import snowflakeInput

snowflake = html.Div(id = "snowflake", children=[   
    snowflakeInput
])