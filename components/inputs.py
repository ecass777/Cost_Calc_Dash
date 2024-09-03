# input components
from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.vars import INSTANCE_LIST

nodesInput = html.Div(id='nodes', children=[
    html.I(id ="nodesIcon", className="fa fa-info-circle me-2"),
    dbc.Tooltip(id ="nodesTooltip",children =[" Excluding Driver Node(s) "], target = "nodesIcon", placement="left"),
    html.Label(id = "nodes-label", children='Nodes in DBX Cluster (Range):'),
    dcc.Input( id= "nodes-input1", value = 1, type = "number"),
    html.Span(" - "),
    dcc.Input( id= "nodes-input2", value = 2, type = "number"),

])

runtimeInput = html.Div(id = 'runtime',children = [
   
    html.Label(id = "runtime-label",children='DBX Runtime (mins):'),
    dcc.Input(id = "runtime-input", value = 60, type = "number"),
])

checkboxInputs = html.Div(id='cluster', children=[

    # First Checkbox with Tooltip
    html.Div([
        html.I(id="jobsIcon", className="fa fa-info-circle me-2"),  # Icon on the left with margin
        dcc.Checklist(
            id='checkbox-options-jobs',
            options=[{'label': 'Jobs Cluster', 'value': 'jobs_cluster'}],
            inputStyle={'margin-right': '10px'},  # Space between checkbox and label
            labelStyle={'display': 'inline-block'}
        )
    ], style={'display': 'flex', 'alignItems': 'center'}),
    dbc.Tooltip(className ="tooltip", children=[html.P(" Jobs clusters are cheaper per DBU and represents 45% "), 
                html.P(" savings of DBX licensing only (i.e. no effect on compute costs) ")]
                , target="jobsIcon", placement="left"),

    # Second Checkbox with Tooltip
    html.Div([
        html.I(id="photonIcon", className="fa fa-info-circle me-2"),  # Icon on the left with margin
        dcc.Checklist(
            id='checkbox-options-photon',
            options=[{'label': 'Photon enabled', 'value': 'photon_enabled'}],
            inputStyle={'margin-right': '10px'}, 
            labelStyle={'display': 'inline-block'}
        )
    ], style={'display': 'flex', 'alignItems': 'center'}),
    dbc.Tooltip(className ="tooltip" ,id="photonTooltip", children = [html.P("  Photon doubles the cost of DBU's consumed, so if it"),
                                                  html.P("does not cut your job runtime in over half, turn it off. ")]
                 , target="photonIcon", placement="left"),

    # Third Checkbox with Tooltip
    html.Div([
        html.I(id="spotIcon", className="fa fa-info-circle me-2"),  # Icon on the left with margin
        dcc.Checklist(
            id='checkbox-options-spot',
            options=[{'label': 'Using SPOT Instance', 'value': 'spot_instance'}],
            inputStyle={'margin-right': '10px'},  # Space between checkbox and label
            labelStyle={'display': 'inline-block'}
        )
    ], style={'display': 'flex', 'alignItems': 'center'}),
    dbc.Tooltip(className = "tooltip",id ="spotTooltip", children =[html.P(" Spot Instance are cheaper compute used intended for non prod / SLA impacting workloads "),
                        html.P(" and represent an ~85% savings on compute costs only(i.e. does not affect DBX license costs) ")], 
                        target="spotIcon", placement="left"),
])

dropdown_list = []
for armSkuName, meterName in INSTANCE_LIST.items():
    dropdown_list.append(armSkuName)


driver_list = dropdown_list.copy()
driver_list.insert(0,"Same as Nodes")



instanceDropdown = html.Div(id="instanceDropdownDiv", children=[
    html.Label(id = "dropdownLabel",children = [
        "Instance:"
    ]),
    dcc.Dropdown(id = "instanceDropdown", options=dropdown_list)
])

driverInstanceDropdown = html.Div(id="driverInstanceDropdownDiv", children=[
    html.Label(id = "driverDropdownLabel",children = [
        "Driver Instance:"
    ]),
    # dcc.Dropdown(options=[dropdown_list.append("Same as Nodes")])
    dcc.Dropdown(id = "driverDropdown", options=driver_list, value = "Same as Nodes")
])

inputLayout = html.Div(id = "inputParentDiv",children = [ html.Div(id = "inputsDiv", children = [
    html.H2('Please provide the following info:'),
    nodesInput,
    runtimeInput,
    checkboxInputs, 
    instanceDropdown,
    driverInstanceDropdown,
    html.Div(id='error-message', style={'color': 'red'}),
    html.H2(id ="total_cost"),
    html.Div(id = "spot-message", style ={'color': '#1D7239'}),

])])