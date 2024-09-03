# Databricks notebook source
# MAGIC %md
# MAGIC # Get Azure Spot VM pricing and eviction rate

# COMMAND ----------

# MAGIC %pip install azure-mgmt-compute azure-identity azure-mgmt-resource azure-cli-core azure-mgmt-resourcegraph pyspark pandas

# COMMAND ----------

# Populate the following variables with the locations and VM types you want to query
# DBU count can be found here: https://azure.microsoft.com/en-us/pricing/details/databricks/?cdn=disable
# These values are different if photon is enabled. This script does not support photon.
locations = ["eastus2", "centralus"]
vm_types_with_dbu = {
    'standard_e4as_v4': 1.0,
    'standard_e8as_v4': 2.0,
    'standard_e16as_v4': 4.0,
    'standard_e32as_v4': 8.0,
    'standard_e48as_v4': 12.0,
    'standard_e64as_v4': 16.0,
    'standard_e16s_v3': 4.0,
    'standard_e32s_v3': 8.0,
    'standard_nc24s_v3': 20.0,
    'standard_ds3_v2': 0.75,
    'standard_ds4_v2': 1.5,
    'standard_nc6s_v3': 5.0,
    'standard_d8s_v3': 1.5,
    'standard_e4ds_v4': 1.0,
    'standard_e8ds_v4': 2.0,
    'standard_e16ds_v4': 4.0,
    'standard_e32ds_v4': 8.0,
    'standard_e48ds_v4': 12.0,
    'standard_e64ds_v4': 16.0,
    'standard_e4ds_v5': 1.5,
    'standard_e8ds_v5': 2.75,
    'standard_e16ds_v5': 5.5,
    'standard_e32ds_v5': 11.0,
    'standard_e48ds_v5': 16.5,
    'standard_e64ds_v5': 22.0
}

# COMMAND ----------

import azure.mgmt.resourcegraph as arg
import pandas as pd
import requests
from IPython.display import display
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient

# COMMAND ----------

locations_str = ""
for location in locations:
    if location == locations[-1]:
        locations_str += "'" + location + "'"
    else:
        locations_str += "'" + location + "', "

vm_type_str = ""
vm_type_list = list(vm_types_with_dbu.keys())
for vm_type in vm_type_list:
    if vm_type == vm_type_list[-1]:
        vm_type_str += "'" + vm_type + "'"
    else:
        vm_type_str += "'" + vm_type + "', "


# COMMAND ----------

credential = DefaultAzureCredential()

# COMMAND ----------

# Get all subscriptions
def get_subscriptions():
    subsClient = SubscriptionClient(credential)
    subsRaw = []
    for sub in subsClient.subscriptions.list():
        subsRaw.append(sub.as_dict())
    subsList = []
    for sub in subsRaw:
        subsList.append(sub.get('subscription_id'))
    return subsList

# COMMAND ----------

def requests_get_resources(str_query, subs_list):
    headers = {"Authorization": "Bearer " + credential.get_token("https://management.azure.com/").token}
    json_body = {"query": str_query, "options": {"resultFormat": "objectArray"}}
    response = requests.post(
        "https://management.azure.com/providers/Microsoft.ResourceGraph/resources?api-version=2021-03-01",
        headers=headers, json=json_body)
    response.raise_for_status()
    return response.json()

# COMMAND ----------

query = f"SpotResources  | where type =~ 'microsoft.compute/skuspotpricehistory/ostype/location' | where sku.name in~ " \
        f"({vm_type_str}) | where properties.osType =~ 'linux' | where location in~ ({locations_str}) | project " \
        f"skuName = tostring(sku.name), osType = tostring(properties.osType), location, latestSpotPriceUSD = " \
        f"todouble(properties.spotPrices[0].priceUSD) | order by latestSpotPriceUSD asc | join kind=inner  (" \
        f"SpotResources | where type =~ 'microsoft.compute/skuspotevictionrate/location' | where sku.name in~ (" \
        f"{vm_type_str}) | where location in~ ({locations_str}) | project skuName = tostring(sku.name), location, " \
        f"spotEvictionRate = tostring(properties.evictionRate) | order by skuName asc, location asc) on skuName, " \
        f"location | project-away skuName1, location1"
subscriptions = get_subscriptions()
data = requests_get_resources(query, subs_list=subscriptions)
for vm in data['data']:
    vm['dbu/hr.'] = vm_types_with_dbu[vm['skuName']]


print(data)

# # COMMAND ----------

# df = pd.DataFrame(data['data'])
# display(df)

# # COMMAND ----------

# df.to_csv('spot_vm_pricing.csv', index=False)
