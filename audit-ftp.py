# -*- coding: utf-8 -*-
"""
2020
@author: wuffalo
"""

import config_sftp
import pandas as pd
import os
import sys
import pysftp
import shutil

def listOfTuples(l1, l2, l3): 
    return list(map(lambda x, y, z:(x,y,z), l1, l2, l3)) 

cnopts = pysftp.CnOpts()
cnopts.hostkeys.load(config_sftp.host_file)

stfp_host = config_sftp.host
sftp_name = config_sftp.username
sftp_port = config_sftp.port
sftp_pw = config_sftp.password

path_to_FTP = "/mnt/shared-drive/05 - Office/FTP/FTP Files/"
srcpath = "/mnt/c/Users/WMINSKEY/.pen/ftp-file-practice/downloaded/"

filepath_list = []
fileday_list = []
filesize_list = []

# walk ftp file directory and create list of files
for subdir, dirs, files in os.walk(path_to_FTP):
    for file in files:
        filepath = subdir + os.sep + file
        if filepath.endswith(".csv"):
            fileday = os.path.basename(filepath).strip('.csv')
            filepath_list.append(filepath)
            fileday_list.append(int(fileday))
            filesize = os.stat(filepath).st_size
            filesize_list.append(filesize)

l1 = filepath_list
l2 = fileday_list
l3 = filesize_list

df_local = pd.DataFrame(listOfTuples(l1,l2,l3))

srv = pysftp.Connection(host=stfp_host,username=sftp_name,password=sftp_pw,cnopts=cnopts)

remote = srv.chdir('.')

filepath_list = []
fileday_list = []
filesize_list = []

data = srv.listdir()
data.remove(data[0])

for i in data:
    if i.endswith(".csv"):
        fileday = os.path.basename(i).strip('.csv')
        filepath_list.append(i)
        fileday_list.append(int(fileday))
        filesize = srv.stat(i).st_size
        filesize_list.append(filesize)

l1 = filepath_list
l2 = fileday_list
l3 = filesize_list

df_remote = pd.DataFrame(listOfTuples(l1,l2,l3))

df_local = df_local.rename(columns={0:"full_file", 1:"day_file", 2:"size"})
df_remote = df_remote.rename(columns={0:"full_file", 1:"day_file", 2:"size"})

combined = df_local.merge(df_remote, on='day_file')

#find where local is bigger than remote
local_list = (combined.query('size_x > size_y').day_file).tolist()

#find where remote is bigger than local
remote_list = (combined.query('size_y > size_x').day_file).tolist()

#Go through list of files which are bigger on local than remote. Narrow down to where remote has more rows than local.
# for i in local_list:
#     j = str(i)
#     k = j+'.csv'
#     year = j[:4]
#     month = j[4:6]
#     sheet_local = pd.read_csv(os.path.join("/mnt/shared-drive/05 - Office/FTP/FTP Files/",year,month,k))
#     # print(j)
#     local_index = len(sheet_local.index)
#     srv.get(k, '/mnt/c/Users/WMINSKEY/.pen/ftp-file-practice/downloaded/'+k)
#     sheet_remote = pd.read_csv("/mnt/c/Users/WMINSKEY/.pen/ftp-file-practice/downloaded/"+k)
#     remote_index = len(sheet_remote.index)
#     if remote_index > local_index:
#         print(j)
#         print("Local Index:")
#         print(local_index)
#         print("Remote Index:")
#         print(sheet_remote)

counter = 1
files_to_update = []
local_index_store = []
remote_index_store = []

#Go through list of files which are bigger on remote than local. Narrow down to where remote has more rows than local.
for i in remote_list:
    j = str(i)
    k = j+'.csv'
    year = j[:4]
    month = j[4:6]
    sheet_local = pd.read_csv(os.path.join("/mnt/shared-drive/05 - Office/FTP/FTP Files/",year,month,k), error_bad_lines=False)
    # print(j)
    local_index = len(sheet_local.index)
    srv.get(k, '/mnt/c/Users/WMINSKEY/.pen/ftp-file-practice/downloaded/'+k)
    sheet_remote = pd.read_csv("/mnt/c/Users/WMINSKEY/.pen/ftp-file-practice/downloaded/"+k, error_bad_lines=False)
    remote_index = len(sheet_remote.index)
    if remote_index > local_index:
        # print(j)
        # print("Local Index:")
        # print(local_index)
        # print("Remote Index:")
        # print(remote_index)
        # print(counter)
        counter = counter+1
        files_to_update.append(j)
        local_index_store.append(local_index)
        remote_index_store.append(remote_index)

srv.close()

print(files_to_update)
print(len(files_to_update))

# challenge = 1

# while challenge == 1:
#     query = input("Action for FTP audit program:\n"
#                 "1 - List files needing updating once more.\n"
#                 "2 - Compare file row qty for each local and remote version.\n"
#                 "3 - Update all listed files.\n"
#                 "4 - exit program\n"
#                 "> ")
#     print("You have selected: ", query)

#     if query == "1":
#         print(files_to_update)
#         print(len(files_to_update))
#     elif query == "2":
#         i = 0
#         for i in files_to_update:
#             print(files_to_update[i])
#             print(local_index_store[i])
#             print(remote_index_store[i])
#             i = i+1
#     elif query == "3":
#         for i in files_to_update:
#             j = str(i)
#             k = j+'.csv'
#             year = j[:4]
#             month = j[4:6]
#             origin = '/mnt/c/Users/WMINSKEY/.pen/ftp-file-practice/downloaded/'+k
#             destination = os.path.join("/mnt/shared-drive/05 - Office/FTP/FTP Files/",year,month,k)
#             shutil.copyfile(origin, destination)
#     elif query == "4":
#         break

# remove following block of code to write over for bigger remote files
# for i in files_to_update:
#     j = str(i)
#     k = j+'.csv'
#     year = j[:4]
#     month = j[4:6]
#     origin = '/mnt/c/Users/WMINSKEY/.pen/ftp-file-practice/downloaded/'+k
#     destination = os.path.join("/mnt/shared-drive/05 - Office/FTP/FTP Files/",year,month,k)
#     shutil.copyfile(origin, destination)


[os.remove(os.path.join(srcpath, f)) for f in os.listdir(srcpath) if f.endswith(".csv")]
# for f in os.listdir(srcpath): if f.endswith(".csv"): os.remove(f)
