import requests
import json
from utils.vars import *


# Queries Azures API for Compute Price
def get_compute_hr_via_api(armSkuName, meterName):

    query = f"serviceFamily eq 'Compute' and armRegionName eq 'eastus2' and armSkuName eq '{armSkuName}' and meterName eq '{meterName}' "

    response = requests.get(API_URL, params={'$filter': query})

    json_data= json.loads(response.text)

    filtered_items = []

    for item in json_data.get("Items", []):
        if "reservationTerm" not in item and "Windows" not in item.get("productName", ""):
            filtered_items.append(item)   

    if filtered_items:
        first_item = filtered_items[0]
        unit_price = first_item.get("unitPrice", None)
    else:
        unit_price = None


    print(unit_price)
    return unit_price



# Runs Query for each Instance and stores the Instance Name and Compute Price in api_data.json
def query_and_store_api_data():
    
    compute_hrs = {}
    compute_hrs_spot = {}
    try:
        for armSkuName, meterName in INSTANCE_LIST.items():
            price = get_compute_hr_via_api(armSkuName,meterName)
            compute_hrs[armSkuName] = price

        with open('api_data.json', 'w') as f:
                json.dump(compute_hrs, f)
        print("API data stored successfully.")
        for armSkuName, meterName in SPOT_INSTANCE_LIST.items():
            price = get_compute_hr_via_api(armSkuName,meterName)
            compute_hrs_spot[armSkuName] = price

        with open('spot_api_data.json', 'w') as f:
                json.dump(compute_hrs_spot, f)
        print("API data stored successfully.")
    except Exception as e:
        print("Error: API data not available")




