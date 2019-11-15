# -*- coding: utf-8 -*-
"""
2019
@author: wuffalo
"""

#first 3 options run func for pallet or entry
#SQL query needs dataframe, assumes SQL knowledge, protect from injection?

import pandas as pd
import xlsxwriter
import os
import glob

if os.path.exists("/mnt/c/Users/WMINSKEY/.pen/Breakout_py.xlsx"):
  os.remove("/mnt/c/Users/WMINSKEY/.pen/Breakout_py.xlsx")

test_code = False

if test_code == True:
    path_to_SOS = "/mnt/c/Users/WMINSKEY/.pen/SOS.csv" # change to latest_file
else:
    list_of_files = glob.glob('/mnt/c/Users/WMINSKEY/Downloads/Shipment Order Summary -*.csv') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    path_to_SOS = latest_file

path_to_excel = "/mnt/c/Users/WMINSKEY/.pen/Breakout_py.xlsx"

show_DSLC = True
show_ROANOKE = True
show_RLCA = True
show_WWT = True
show_IngramMX = True

df = pd.read_csv(path_to_SOS)

#columns to delete - INITIAL PASS

df = df.drop(columns=['ORDERKEY','SO','SS','STORERKEY','INCOTERMS','ORDERDATE','ACTUALSHIPDATE','DAYSPASTDUE',
                'PASTDUE','ORDERVALUE','TOTALSHIPPED','EXCEP','STOP','PSI_FLAG','UDFNOTES','INTERNATIONALFLAG',
                'BILLING','LOADEDTIME','UDFVALUE1'])

df = df.rename(columns={'EXTERNORDERKEY':'SO-SS','C_COMPANY':'Customer','ADDDATE':'Add Date','STATUSDESCR':'Status',
                        'TOTALORDERED':'QTY','SVCLVL':'Carrier','EXTERNALLOADID':'Load ID','EDITDATE':'Last Edit',
                        'C_STATE':'State','C_COUNTRY':'Country','Textbox6':'TIS'})

writer = pd.ExcelWriter(path_to_excel, engine='xlsxwriter')

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

#wpp = df.groupby('Pallet_ID')['Weight'].sum()

#wpp.columns = ['Pallet ID','Total Weight']

#wpp.columns('Weight') = wpp

#print(wpp.dtypes)
#print(wpp.ndim)

#wpp.sort()

#print(list(wpp)[10])

#Create DF queries
DSLC = df['TYPEDESCR'] == "DSLC Move"
ROANOKE = df['CUSTID'] == "7128"
# ROANOKE = df[(df['CUSTID'] == '7128') & (df['Carrier'] != 'BNAF*')]
RLCA = df['Carrier'] == "RLCA-LTL-4_DAY"
WWT = df['Carrier'] == "TXAP-TL-STD_WWT"
IngramMX = df['Customer'] == "Interamerica Forwarding C/O Ingram Micro Mexi"

#drop columns - SECOND PASS
df = df.drop(columns=['TYPEDESCR','CUSTID','PROMISEDATE','Last Edit'])
print(df.dtypes)

#Check if dataframes are empty
if DSLC.empty == True:
    show_DSLC = False
if ROANOKE.empty == True:
    show_ROANOKE = False
if RLCA.empty == True:
    show_RLCA = False
if WWT.empty == True:
    show_WWT = False
if IngramMX.empty == True:
    show_IngramMX = False

#Give preview of queries
if test_code == True:
    print("DSLC Orders: \n",df[DSLC].head(2))
    print("Roanoke Orders: \n",df[ROANOKE].head(2))
    print("RLCA Orders: \n",df[RLCA].head(2))
    print("WWT Orders: \n",df[WWT].head(2))
    print("Ingram MX Orders: \n",df[IngramMX].head(2))

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

if show_DSLC == True:
    df[DSLC].to_excel(writer, sheet_name='DSLC')
if show_ROANOKE == True:
    df[ROANOKE].to_excel(writer, sheet_name='Roanoke')
if show_RLCA == True:
    df[RLCA].to_excel(writer, sheet_name='RLCA')
if show_WWT == True:
    df[WWT].to_excel(writer, sheet_name='WWT')
if show_IngramMX == True:
    df[IngramMX].to_excel(writer, sheet_name='IngramMX')

writer.save()