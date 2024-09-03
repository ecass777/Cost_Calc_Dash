# Variables used in calculations
# Only change to reflect changes in discounts or premiums
DBX_DISC = .4
AZURE_DISC = .32
SF_UNIT = 3.04
SF_TB_PER_MONTH = 23
JOBS_DISCOUNT = .46
PHOTON_PREMIUM = 2
DBU_COST = .55
JOB_COST = .3
API_URL = "https://prices.azure.com/api/retail/prices"


# (from Azure API: https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices )
# Format:
# armSkuName : meterName
INSTANCE_LIST = {
    "Standard_E4as_v4": "E4as v4",
    "Standard_E4ds_v4": "E4ds v4",
    "Standard_E4ds_v5": "E4ds v5",
    "Standard_E8as_v4": "E8as v4",
    "Standard_E8ds_v4": "E8ds v4",
    "Standard_E16as_v4": "E16as v4",
    "Standard_E16ds_v4": "E16ds v4",
    "Standard_E16ds_v5": "E16ds v5",
    "Standard_E32as_v4": "E32as v4",
    "Standard_E32as_v5": "E32as v5",
    "Standard_E32ds_v4": "E32ds v4",
    "Standard_E32ds_v5": "E32ds v5",
    "Standard_E64as_v4": "E64as v4",
    "Standard_E64ds_v4": "E64ds v4",
    "Standard_E64ds_v5": "E64ds v5",
}

SPOT_INSTANCE_LIST = {

    "Standard_E4as_v4": "E4as v4 Spot",
    "Standard_E4ds_v4": "E4ds v4 Spot",
    "Standard_E4ds_v5": "E4ds v5 Spot",
    "Standard_E8as_v4": "E8as v4 Spot",
    "Standard_E8ds_v4": "E8ds v4 Spot",
    "Standard_E16as_v4": "E16as v4 Spot",
    "Standard_E16ds_v4": "E16ds v4 Spot",
    "Standard_E16ds_v5": "E16ds v5 Spot",
    "Standard_E32as_v4": "E32as v4 Spot",
    "Standard_E32as_v5": "E32as v5 Spot",
    "Standard_E32ds_v4": "E32ds v4 Spot",
    "Standard_E32ds_v5": "E32ds v5 Spot",
    "Standard_E64as_v4": "E64as v4 Spot",
    "Standard_E64ds_v4": "E64ds v4 Spot",
    "Standard_E64ds_v5": "E64ds v5 Spot",

}