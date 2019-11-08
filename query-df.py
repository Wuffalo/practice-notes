# -*- coding: utf-8 -*-
"""
2019
@author: wuffalo
"""

#first 3 options run func for pallet or entry
#SQL query needs dataframe, assumes SQL knowledge, protect from injection?

import pandas as pd
#import pandasql
#from pandasql import sqldf
#pysqldf = lambda q: sqldf(q, globals())

path_to_csv = "/mnt/c/Users/WMINSKEY/.pen/FTP-Project/20191030.csv"

df = pd.read_csv(path_to_csv)

# print(df.head(5))

# print(df.tail(2))

# print(df.shape)     #   (rows, columns)
# print(df.ndim)      #   number of dimensions
print(df.dtypes)    #   list columns and assumed data type
# print(df['Weight'].describe())
# print(df['Product'].describe())

# #  3 ways to select a column
# print(df.END_CUSTOMER_NAME.head(2))
# print(df['END_CUSTOMER_NAME'].head(2))
# print(df.iloc[:,9].head(2))

# # select multiple columns
# print(df[['Weight', 'Pallet_ID']])
# print(df.iloc[:, [6,0]])

wpp = df.groupby('Pallet_ID')['Weight'].sum()

#wpp.columns = ['Pallet ID','Total Weight']

#wpp.columns('Weight') = wpp

print(wpp.dtypes)
print(wpp.ndim)

#wpp.sort()

#print(wpp.head(10))

#print(list(wpp)[10])

print(wpp.head(2))

### Filter columns
#   Search integer column for match #
#interesting_SO = df['Sales_Order'] == 108906178
#print(df[interesting_SO])

#   Search integer column for comparison    #
#heavy = df['Weight'] > 500
#print(df[heavy])

#   Search object for string exact match  #
#interesting_product = df['Product'] == "AIR-CT5520-K9"
#print(df[interesting_product])

#   Search Object for string    #
#London = df['END_CUSTOMER_ADDRESS'].str.contains('LONDON')
#print(df[London])

#   Print search terms combination  #
#print(df[interesting_SO & heavy])
###     

# query = input("Enter your query input for the Master FTP file\n"
#               "1 - PalletID\n"
#               "2 - Carton ID\n"
#               "3 - SO-SS\n"
#               "4 - SQL Query\n"
#               "> ")
# print("You have selected: ", query)

# if query == "1":
#     PalletID = input("Enter in your Pallet ID: ")
#     print("You entered the pallet ID of: ", PalletID)
#     print(MFTP.query('Pallet_ID == PalletID', inplace = True))
# elif query == "2":
#     CartonID = input("Enter in your carton ID (CID): ")
#     print("You entered CID: ", CartonID)
# elif query =="3":
#     SOSS = input("Enter in your SO-SS: ")
#     print("You entered in the SO-SS: ", SOSS)
# elif query =="4":
#     SQY = input("Enter SQL query: ")
#     print("You entered SQL: ", SQY)