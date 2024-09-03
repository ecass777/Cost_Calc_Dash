from app import app
from dash import callback,Output,Input,State, no_update, callback_context, html
from openpyxl import load_workbook
from components.tables import build_instance_table
from calculations.databricks import calculate_total,calculate_spot_discount


# Callback that takes inputs and automatically generates a table of Compute Prices as soon as the inputs change
@app.callback(
    [Output('total_cost_table', 'children'),
     Output('total_cost', 'children'),
     Output('error-message', 'children'),
     Output("spot-message", "children"),
     Output("table-message", "children")],
    Input('nodes-input1', 'value'),
    Input('nodes-input2', 'value'),
    Input('runtime-input', 'value'),
    Input('checkbox-options-jobs', 'value'),
    Input('checkbox-options-photon', 'value'),
    Input('checkbox-options-spot', 'value'),
    Input('instanceDropdown', 'value'),
    Input('driverDropdown', 'value')
)

def get_values(nodes_value_low,nodes_value_high, runtime_value, is_cluster,is_photon_enabled,using_spot_instance,instance_dropdown,driver_dropdown):

    spot_message = ""
    table_message = ""

    # does not run callback if either of the input fields are empty
    if not nodes_value_low or not nodes_value_high or not runtime_value or not instance_dropdown:
        return no_update, no_update, "", spot_message, table_message
    
    if nodes_value_low > nodes_value_high:
        return no_update, no_update, html.H2("Error: The minimum nodes value cannot be greater than the maximum nodes value."), spot_message, table_message

    
    # looking for checkbox options
    if is_cluster is None:
        is_cluster = []

    if is_photon_enabled is None:
        is_photon_enabled = []

    if using_spot_instance is None:
        using_spot_instance= []

    is_cluster = 'jobs_cluster' in is_cluster
    is_photon_enabled = 'photon_enabled' in is_photon_enabled
    using_spot_instance = 'spot_instance' in using_spot_instance

    cost = calculate_total(using_spot_instance,is_photon_enabled,is_cluster,nodes_value_low,nodes_value_high,runtime_value,instance_dropdown, driver_dropdown)

    total_cost = f"Total Cost : {cost}"

    if not using_spot_instance:
        spot_discount = calculate_spot_discount(is_photon_enabled,is_cluster, nodes_value_high, runtime_value, instance_dropdown)
        spot_message = html.H4(f"You could save up to ${spot_discount} by using Spot Instances")
        
    table_message ="Alternative Instances and their Costs (Assuming same driver configuration):"
    # function to build compute price table
    table = build_instance_table(using_spot_instance,nodes_value_low,nodes_value_high,runtime_value,is_photon_enabled,is_cluster, driver_dropdown)

    return table, total_cost, "", spot_message, table_message
