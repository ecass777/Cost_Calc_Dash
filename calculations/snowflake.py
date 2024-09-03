from utils.vars import *


def calculate_snowflake_compute(warehouse,runtime):
    credits_per_hour = 0
    if warehouse == "XS":
        credits_per_hour = 1
    elif warehouse == "S": 
        credits_per_hour = 2
    elif warehouse == "M": 
        credits_per_hour = 4
    elif warehouse == "L": 
        credits_per_hour = 8
    elif warehouse == "XL": 
        credits_per_hour = 16
    elif warehouse == "2XL": 
        credits_per_hour = 32
    elif warehouse == "3XL": 
        credits_per_hour = 64

    compute_cost = (credits_per_hour *(SF_UNIT) * (runtime/60))

    return round(compute_cost, 2)
    
def calculate_storage_per_month(size):
    cost_per_month = (SF_TB_PER_MONTH * size)

    return round(cost_per_month, 2)