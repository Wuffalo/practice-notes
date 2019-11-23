# -*- coding: utf-8 -*-
"""
2019
@author: wuffalo
"""

import pandas as pd
import numpy as np
import xlsxwriter
import os
import glob

path_to_excel = "/mnt/c/Users/WMINSKEY/Output/Master_FTP.csv"

df = pd.read_csv(path_to_excel, parse_dates=[7,8], infer_datetime_format=True)

# print(df.shape)     #   (rows, columns)
# print(df.ndim)      #   number of dimensions
# print(df.dtypes)    #   list columns and assumed data type
# print(df['Weight'].describe())
# print(df['Product'].describe())

#drop extra columns
df.drop(df.iloc[:,16:], inplace=True, axis=1)

#creates SO-SS column by combining sales order and ship set
df['SO-SS'] = df['Sales_Order'].astype(str) + '-' + df['Ship_Set'].astype(str)

# print(df.dtypes)
# print(df.head(2))
# print(df.tail(2))

# print(df['Pallet_ID'].describe())
# print(df['Carton_ID'].describe())
# print("")
# print(df['Product'].describe())
# print(df['MESSAGE_ID'].describe())
# print(df['SO-SS'].describe())
# print(df['Pallet_LastEditDt'].describe())
# print(df['ASN_Date_Time'].describe())
# print(df['FTPday'].describe())
# print(df['FTPsize'].describe())

# #  3 ways to select a column
# print(df.END_CUSTOMER_NAME.head(2))
# print(df['END_CUSTOMER_NAME'].head(2))
# print(df.iloc[:,9].head(2))

# # select multiple columns
# print(df[['Weight', 'Pallet_ID']])
# print(df.iloc[:, [6,0]])

#wpp = df.groupby('Pallet_ID')['Weight'].sum()

#wpp.columns = ['Pallet ID','Total Weight']

#wpp.columns('Weight') = wpp

#print(wpp.dtypes)
#print(wpp.ndim)

#wpp.sort()

#print(list(wpp)[10])

#isolate file where extra column was added#
# df['Unnamed: 17'].replace('', np.nan, inplace=True)
# df.dropna(subset=['Unnamed: 17'], inplace=True)
# print(df['FTPday'])

# dupes = df['Carton_ID'] == "Carton_ID"

# print(df[dupes])

# df = df.drop(df[(df.score < 50) & (df.score > 20)].index)
#delete where multiple headers
df.drop(df[df.Carton_ID == "Carton_ID"].index, inplace=True)

# print(df['END_CUSTOMER_ADDRESS'].head(5))

#include na=False because some values are NaN, prevents error by assuming NaN is blank
# iFlowStatus = Sales[Sales['Product'].str.contains('iFlow', na=False)]['Status']
# London = df[df['END_CUSTOMER_ADDRESS'].str.contains('~IN~', na=False)]['END_CUSTOMER_ADDRESS']
# print(df[London])

# #Create DF queries
# DSLC = df['TYPEDESCR'] == "DSLC Move"
# ROANOKE = df['CUSTID'] == "7128"
# # ROANOKE = df[(df['CUSTID'] == '7128') & (df['Carrier'] != 'BNAF*')]
# RLCA = df['Carrier'] == "RLCA-LTL-4_DAY"
# WWT = df['Carrier'] == "TXAP-TL-STD_WWT"
# IngramMX = df['Customer'] == "Interamerica Forwarding C/O Ingram Micro Mexi"

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

x = 1

while x == 1:
    query = input("Enter your query input for the Master FTP file\n"
                "1 - PalletID\n"
                "2 - Carton ID\n"
                "3 - SO-SS\n"
                "4 - SQL Query\n"
                "5 - exit program"
                "> ")
    print("You have selected: ", query)

    if query == "1":
        PalletID = input("Enter in your Pallet ID: ")
        print("You entered the pallet ID of: ", PalletID)
        PLout = df['Pallet_ID'] == PalletID
        print(df[PLout])
    elif query == "2":
        CartonID = int(input("Enter in your carton ID (CID): "))
        print("You entered CID: ", CartonID)
        CIDout = df['Carton_ID'] == CartonID
        print(df[CIDout])
    elif query =="3":
        SOSS = input("Enter in your SO-SS: ")
        print("You entered in the SO-SS: ", SOSS)
        SOSSout = df['SO-SS'] == SOSS
        print(df[SOSSout])
    elif query =="5":
        break

# elif query =="4":
#     SQY = input("Enter SQL query: ")
#     print("You entered SQL: ", SQY)