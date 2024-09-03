# NOT USED AS OF NOW, MAY BE USED FOR FUTURE FEATURES



# import pandas as pd
# import numpy as np
# from openpyxl import load_workbook

# def getTables():
#     data = {}
#     with pd.ExcelFile("assets/CCCv2.xlsx") as xls:
#         data["Databricks Calculator"] = pd.read_excel(xls, "Databricks Calculator",skiprows=(10), index_col= None,
#                                                     usecols="B:M",
#                                                      engine = 'openpyxl')

#     data["Databricks Calculator"] = data["Databricks Calculator"].map(
#         lambda x: round(x, 2) if isinstance(x, (int, float)) else x
#     )


#     return data

# def inputValue(sheet, value, cell):
#     import os
#     if os.path.exists("assets/CCCv2.xlsx"):

#         print(os.path.exists("assets/CCCv2.xlsx"))
#         wb = load_workbook("assets/CCCv2.xlsx")
#         ws = wb[sheet]
#         ws[cell].value = value
#         wb.save("assets/CCCv2.xlsx")

#         return "Updated!"
#     else:
#         print("PATH DNE")
#         print(os.path.exists("assets/CCCv2.xlsx"))
