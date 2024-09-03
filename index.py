from app import app
from components.layout import layout
from utils.azure_api import query_and_store_api_data
import callbacks
from pages.dbx import dbx
from pages.snowflake import snowflake
from dash import Output, Input

app.layout = layout

app._favicon = "favicon.ico"

# Query API rates when app is intialized.  Stored in api_data.json
query_and_store_api_data()

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return dbx
    elif tab == 'tab-2':
        return snowflake
    elif tab == 'tab-3':
        return "AKS!"

if __name__ == "__main__":
    app.run_server(debug=True)
