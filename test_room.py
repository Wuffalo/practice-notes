# -*- coding: utf-8 -*-
"""
2019
@author: wuffalo
"""

import config_sftp
import pandas as pd
import os
import sys
import pysftp

cnopts = pysftp.CnOpts()
cnopts.hostkeys.load(config_sftp.host_file)

stfp_host = config_sftp.host
sftp_name = config_sftp.username
sftp_port = config_sftp.port
sftp_pw = config_sftp.password

# srv = pysftp.Connection(host=stfp_host,username=sftp_name,password=sftp_pw,cnopts=cnopts)

# srv.close()

def listOfTuples(l1, l2, l3): 
    return list(map(lambda x, y, z:(x,y,z), l1, l2, l3)) 

path_to_FTP = "/mnt/shared-drive/05 - Office/FTP/FTP Files/"
path_to_record = '/mnt/shared-drive/05 - Office/OTS/Wolf/list.csv'

if os.path.exists(path_to_record):
    df_record = pd.read_csv(path_to_record)
    file_list = df_record['full_file'].tolist()
    new_list_needed = False
    # df_record = df_record.rename(columns={'0':"full_file", '1':"day_file", '2':"size"})
else: 
    file_list = []
    new_list_needed = True

# def GetHumanReadable(size,precision=2):
#     suffixes=['B','KB','MB','GB','TB']
#     suffixIndex = 0
#     while size > 1024 and suffixIndex < 4:
#         suffixIndex += 1 #increment the index of the suffix
#         size = size/1024.0 #apply the division
#     return "%.*f%s"%(precision,size,suffixes[suffixIndex])

filepath_list = []
fileday_list = []
filesize_list = []

# walk file directory and create list of files
for subdir, dirs, files in os.walk(path_to_FTP):
    for file in files:
        filepath = subdir + os.sep + file
        if filepath.endswith(".csv"):
            if filepath not in file_list:
                fileday = os.path.basename(filepath).strip('.csv')
                filepath_list.append(filepath)
                fileday_list.append(int(fileday))
                filesize = os.stat(filepath).st_size
                filesize_list.append(filesize)

l1 = filepath_list
l2 = fileday_list
l3 = filesize_list

df_scan = pd.DataFrame(listOfTuples(l1,l2,l3))

# df_diff = pd.concat([df_scan, df_record])
# df_diff = df_diff.reset_index(drop=True)

# df_gpby = df_diff.groupby(list(df_diff.columns))

# idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1]
# print(df_diff.reindex(idx))

# df_scan.to_csv('/mnt/shared-drive/05 - Office/OTS/Wolf/list.csv', index=False)
# print("Scanned df")
# df_scan = df_scan.rename(columns={0:"full_file", 1:"day_file", 2:"size"})
# print(df_scan.dtypes)
# print(df_scan.ndim)
# print(df_scan.head(2))
# print(df_scan.tail(2))
# print(df_scan['day_file'].head(5))

# print("Imported stored df")
# df_record = df_record.rename(columns={'0':"full_file", '1':"day_file", '2':"size"})
# print(df_record.dtypes)
# print(df_record.ndim)
# print(df_record.head(2))
# print(df_record.tail(2))
# print(df_record['day_file'].head(5))

# print("Printing df_scan column names")
# print(df_scan.columns)
# print("Printing df_record column names")
# print(df_record.columns)

# df_out = pd.concat([df_scan,df_record],axis=1).drop_duplicates(keep=False) # combines two dataframes and removes duplicates, leaves 1 example of each
# common = df_scan.merge(df_record, on='day_file')

# common = pd.merge()

# df1[(~df1.col1.isin(common.col1))&(~df1.col2.isin(common.col2))]
if new_list_needed == True:
    df_scan = df_scan.rename(columns={0:"full_file", 1:"day_file", 2:"size"})
    df_scan.to_csv(path_to_record, index=False)
    print("New list of FTP files created at "+'\''+path_to_record+'\'.')
elif new_list_needed == False:
    df_scan = df_scan.rename(columns={0:"full_file", 1:"day_file", 2:"size"})
    df_out = df_scan[~df_scan.isin(df_record)].dropna()
    if df_out.empty == True:
        print("Nothing to download.")
    else:
        print("Need to download the following FTP days:")
        print(df_out.day_file)

'''
df_list = []

# for each file name, grab file, format and append to list of dataframes
for f in file_list:
    sheet = pd.read_csv(f, error_bad_lines=False)
    f_source = os.path.basename(f).strip('.csv')
    sheet["FTPday"] = f_source
    b_size = os.stat(f).st_size
    sheet["FTPsize"] = b_size
    df_list.append(sheet)

Master_FTP = pd.concat(df_list, ignore_index=True, sort=False)

Master_FTP.to_csv('C:/Users/WMINSKEY/Output/Master_FTP.csv',index=False)
'''

# import time
# time.process_time() # gives current process time, clocks of cpu run
# time.time() # gives actual current clock time to nanosecond degree

# print(df.shape)     #   (rows, columns)
# print(df.ndim)      #   number of dimensions
# print(df.dtypes)    #   list columns and assumed data type
# print(df['Weight'].describe())
# print(df['Product'].describe())

#drop extra columns
# df.drop(df.iloc[:,16:], inplace=True, axis=1)

#creates SO-SS column by combining sales order and ship set
# df['SO-SS'] = df['Sales_Order'].astype(str) + '-' + df['Ship_Set'].astype(str)

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
# df.drop(df[df.Carton_ID == "Carton_ID"].index, inplace=True)

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

# x = 1

# while x == 1:
#     query = input("Enter your query input for the Master FTP file\n"
#                 "1 - PalletID\n"
#                 "2 - Carton ID\n"
#                 "3 - SO-SS\n"
#                 "4 - SQL Query\n"
#                 "5 - exit program"
#                 "> ")
#     print("You have selected: ", query)

#     if query == "1":
#         PalletID = input("Enter in your Pallet ID: ")
#         print("You entered the pallet ID of: ", PalletID)
#         PLout = df['Pallet_ID'] == PalletID
#         print(df[PLout])
#     elif query == "2":
#         CartonID = int(input("Enter in your carton ID (CID): "))
#         print("You entered CID: ", CartonID)
#         CIDout = df['Carton_ID'] == CartonID
#         print(df[CIDout])
#     elif query =="3":
#         SOSS = input("Enter in your SO-SS: ")
#         print("You entered in the SO-SS: ", SOSS)
#         SOSSout = df['SO-SS'] == SOSS
#         print(df[SOSSout])
#     elif query =="5":
#         break