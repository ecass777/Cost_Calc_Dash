from app import app
from dash import callback, Input, Output, no_update
from calculations.snowflake import calculate_snowflake_compute, calculate_storage_per_month

@app.callback(
    [Output('compute_cost','children'),
     Output('storage_per_month', 'children')],
     Input('warehouseDropdown', 'value'),
     Input("runtime-input", 'value'),
     Input('dataSizeInput',"value")
)
def snowflake_calculator(warehouse, runtime, datasize):
    print("triggered!")

    sf_compute = calculate_snowflake_compute(warehouse, runtime)

    storage = calculate_storage_per_month(datasize)

    return f"Compute Cost: ${sf_compute}", f"Storage Cost Per Month: ${storage}"