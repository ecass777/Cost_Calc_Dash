from dash import html, dcc, dash_table
from calculations.databricks import calculate_spot_cost, calculateDBXLicenseCost
from utils.vars import INSTANCE_LIST
import pandas as pd

def build_instance_table(using_spot_instance, nodes_value_low, nodes_value_high, runtime_value, is_photon_enabled, is_cluster, driver):

    instance_costs = []
    # iterates through Instances to get data for cost table
    for armSkuName, meterName in INSTANCE_LIST.items():
        driver_cost = 0
        if driver == "Same as Nodes":
            driver_cost = (calculate_spot_cost(False,1,runtime_value,armSkuName) 
            + calculateDBXLicenseCost(runtime_value, is_photon_enabled, is_cluster, 1, armSkuName))
        else:
            driver_cost = (calculate_spot_cost(False,1,runtime_value,driver) 
                       + calculateDBXLicenseCost(runtime_value, is_photon_enabled, is_cluster, 1, driver))
        # Calculate cost for the lower node value
        spot_cost_low = calculate_spot_cost(using_spot_instance, nodes_value_low, runtime_value, armSkuName)
        db_license_cost_low = calculateDBXLicenseCost(runtime_value, is_photon_enabled, is_cluster, nodes_value_low, armSkuName)
        total_cost_low = round((spot_cost_low + db_license_cost_low + driver_cost), 2)
        # formatted_spot_cost_low = f"${spot_cost_low:,.2f}"
        # formatted_dbl_cost_low = f"${db_license_cost_low:,.2f}"
        formatted_total_cost_low = f"${total_cost_low:,.2f}"

        # Calculate cost for the higher node value
        spot_cost_high = calculate_spot_cost(using_spot_instance, nodes_value_high, runtime_value, armSkuName)
        db_license_cost_high = calculateDBXLicenseCost(runtime_value, is_photon_enabled, is_cluster, nodes_value_high, armSkuName)
        total_cost_high = round((spot_cost_high + db_license_cost_high +driver_cost), 2)
        # formatted_spot_cost_high = f"${spot_cost_high:,.2f}"
        # formatted_dbl_cost_high = f"${db_license_cost_high:,.2f}"
        formatted_total_cost_high = f"${total_cost_high:,.2f}"

        formatted_driver_cost = round(driver_cost, 2)
        # Store the formatted cost range
        instance_costs.append({
            'Instance Type': armSkuName,
            'Effective Compute per VM': f"${spot_cost_low:,.2f} - ${spot_cost_high:,.2f}",
            'DBX License Cost': f"${db_license_cost_low:,.2f} - ${db_license_cost_high:,.2f}",
            'Driver Cost' : f"${formatted_driver_cost}",
            'Total Cost': f"{formatted_total_cost_low} - {formatted_total_cost_high}"

        })

    # Create a DataFrame with the instance costs
    df = pd.DataFrame(instance_costs)


    # Generate the DataTable component
    table = dash_table.DataTable(
        id="cost_table",
        data=df.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in df.columns],
        style_table={'overflowX': 'auto'},  # Ensure horizontal scrolling if needed
        style_header={
            'fontWeight': 'bold',  
            'backgroundColor': '#BFB3EF',  
            'color': 'black',  
            'textAlign': 'center'  
        },
         style_data_conditional=[
            # Bold specific columns
            {
                'if': {'column_id': 'Total Cost'},
                'fontWeight': 'bold',
                'color': '#36A824',
                'backgroundColor': '#f0f0f0'
            },
            {
                'if': {'column_id': 'Instance Type'},
                'fontWeight': 'bold',
            },
        ],
    )
    
    # Return the table inside a Div
    return html.Div(id="price_tables", children=[table])

# DEBUGGING

# def test_costs(using_spot_instance, nodes_value, runtime_value, is_photon_enabled, is_cluster):
#     instance_costs = {}


#     for armSkuName, meterName in INSTANCE_LIST.items():
#         spot_cost = calculate_spot_cost(using_spot_instance, nodes_value, runtime_value, armSkuName, meterName)
#         db_license_cost = calculateDBXLicenseCost(runtime_value, is_photon_enabled, is_cluster, nodes_value, armSkuName, meterName)
#         total_cost = spot_cost + db_license_cost

#         instance_costs[armSkuName]= total_cost
#     print(instance_costs)

# test_costs(True,11,60,True,True)