from dash import dcc, html

warehouseInput = html.Div(id ="warehouse", children =[
    html.Label("Warehouse Size:"),
    dcc.Dropdown(id ="warehouseDropdown", options = ["XS", "S","M","L", "XL", "2XL", "3XL"])
])

runtimeInput = html.Div(id = 'runtime',children = [
    html.Label(id = "runtime-label",children='Snowflake Runtime (mins):'),
    dcc.Input(id = "runtime-input", value = 60, type = "number"),
])

sizeInput = html.Div(id = "dataSize", children =[
    html.Label(id = "dataSizeLabel",children = ["Storage Size (TB):"]),
    dcc.Input(id = "dataSizeInput", value = 1, type ="number")
])

snowflakeInput = html.Div(id ="sfInputParentDiv",children = [
    html.H2("Please provide the following info:"),
    warehouseInput, 
    runtimeInput,
    sizeInput,
    html.H3(id = "compute_cost"),
    html.H3(id= "storage_per_month")
])