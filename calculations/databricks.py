from utils.vars import *
from utils.azure_api import get_compute_hr_via_api
import json

# Fetches compute hour from json file: api_data.json
def get_compute_hr_via_json(armSkuName, spot):
    print(armSkuName)
    try:
        if spot:
            with open('spot_api_data.json', 'r') as f:
                compute_hrs = json.load(f)
                compute_hr = compute_hrs.get(armSkuName)
        else:
            with open('api_data.json', 'r') as f:
                compute_hrs = json.load(f)

            compute_hr = compute_hrs.get(armSkuName)

        print(compute_hr)
    except Exception as e:
        print("Error:" , Exception)
    return compute_hr

# Factors in if it is a job cluster, if it is using photon, and the DataBricks Discount (40% as of August 2024)
def dbu_per_hour(cluster, job_cost, dbu_cost, nodes, photon, photon_premium, dbx_disc):
    if cluster:
        cost = job_cost
    else:
        cost = dbu_cost    
    cost *= nodes

    if photon:
        cost*= photon_premium

    cost *= (1-dbx_disc)
    return cost

# Factors in Azure Discout of 32% (As of August 2024)
def calc_compute_hr_discount(nodes,azure_disc, armSkuName,spot):
    compHr = (get_compute_hr_via_json(armSkuName, spot) * nodes)
    compHrDisc = compHr * (1-azure_disc)
    return compHrDisc

# Calclualtes DBU License Multiplier based off of compute Hour
# Returns DataBricks License Cost by multiplying the DBU Hours by the multiplier
def calculateDBXLicenseCost(runtime, Photon, cluster, nodes, armSkuName):
    multiplier = (get_compute_hr_via_json(armSkuName,False) / .252)
    dbuPerHour = dbu_per_hour(cluster,JOB_COST,DBU_COST,nodes,Photon,PHOTON_PREMIUM,DBX_DISC)
    output = (dbuPerHour * (runtime/60) * multiplier)
    return output

def calculate_spot_cost(spot, nodes, runtime, armSkuName):
    computeHrDiscount = calc_compute_hr_discount(nodes,AZURE_DISC, armSkuName, spot)
    cost = computeHrDiscount * (runtime / 60)

    return cost

def calculate_total(using_spot_instance, is_photon_enabled,is_cluster,nodes_value_low,nodes_value_high,runtime_value, armSkuName, driver):
    driver_cost = 0
    if driver == "Same as Nodes":
        driver_cost = (calculate_spot_cost(False,1,runtime_value,armSkuName) 
        + calculateDBXLicenseCost(runtime_value, is_photon_enabled, is_cluster, 1, armSkuName))
    else:
        driver_cost = (calculate_spot_cost(False,1,runtime_value,driver) 
                       + calculateDBXLicenseCost(runtime_value, is_photon_enabled, is_cluster, 1, driver))
        print(driver_cost)
        
    spot_cost_low = (calculate_spot_cost(using_spot_instance, nodes_value_low, runtime_value, armSkuName))
    db_license_cost_low = (calculateDBXLicenseCost(runtime_value, is_photon_enabled, is_cluster, nodes_value_low, armSkuName))
    total_cost_low = round((spot_cost_low + db_license_cost_low + driver_cost), 2)


    # debugging
    # print("looping")
    spot_cost_high = (calculate_spot_cost(using_spot_instance, nodes_value_high, runtime_value, armSkuName))
    db_license_cost_high = (calculateDBXLicenseCost(runtime_value, is_photon_enabled, is_cluster, nodes_value_high, armSkuName))
    total_cost_high = round((spot_cost_high+ db_license_cost_high + driver_cost), 2)


    total_cost_range = str(f"${total_cost_low} - ${total_cost_high}")

    return total_cost_range

def calculate_spot_discount( is_photon_enabled,is_cluster,nodes,runtime_value, armSkuName):
    spot_cost_no_spot = (calculate_spot_cost(False, nodes, runtime_value, armSkuName))
    db_license_cost_no_spot = (calculateDBXLicenseCost(runtime_value, is_photon_enabled, is_cluster, nodes, armSkuName))
    total_cost_no_spot = round((spot_cost_no_spot + db_license_cost_no_spot), 2)

    spot_cost_with_spot =(calculate_spot_cost(True, nodes, runtime_value, armSkuName))
    db_license_cost_with_spot = (calculateDBXLicenseCost(runtime_value, is_photon_enabled, is_cluster, nodes, armSkuName))
    total_cost_with_spot = round((spot_cost_with_spot + db_license_cost_with_spot), 2)

    spot_discount = round(total_cost_no_spot - total_cost_with_spot, 2)

    return spot_discount








# print("SPOT:" , calculate_spot_cost(True,10,100))

# print("DB License:" , calculateDBLicenseCost(100,True,True,10))




