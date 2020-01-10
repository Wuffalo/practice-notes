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

# combined = pd.concat([df_local, df_remote], ignore_index=True, sort=False)

combined = df_local.merge(df_remote, on='day_file')

# print(combined.head(1))
# print(combined.tail(1))

# print(combined.ndim)
# print(combined.columns)
# print(combined.dtypes)
# print(combined.shape)

#find where local is bigger than remote
# print(combined.query('size_x > size_y').day_file)
local_list = (combined.query('size_x > size_y').day_file).tolist()
# print(local_list[:3])

#find where remote is bigger than local
# print(combined.query('size_y > size_x').day_file)
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
files_to_dl = []

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
        print(j)
        print("Local Index:")
        print(local_index)
        print("Remote Index:")
        print(remote_index)
        print(counter)
        counter = counter+1
        files_to_dl.append(j)

srv.close()

print(files_to_dl)
print(len(files_to_dl))

# for root, subFolders, files in os.walk(srcpath):
#     for file in files:
#         subFolder = os.path.join(destpath, file[:4], file[4:6])
#         if os.path.exists(os.path.join(subFolder, file)):
#             if (int(os.stat(os.path.join(root, file)).st_size) - int(os.stat(os.path.join(subFolder, file)).st_size)) > 0:
#                 shutil.copy2(os.path.join(root, file), subFolder)
#         else:
#             shutil.copy2(os.path.join(root, file), subFolder)

# dfl = df_local['day_file']
# dfr = df_remote['day_file']

# df_out = dfr[~dfr.isin(dfl)].dropna()

# if df_out.empty == True:
#     srv.close()
#     print("Nothing to update.")
#     print(df_local['day_file'].tail(1))
#     print(df_remote['day_file'].tail(1))
# else:
#     for i in df_out:
#         j = (str(i)+'.csv')
#         srv.get(j, '/mnt/c/Users/WMINSKEY/.pen/ftp-file-practice/downloaded/'+j)
#         print("Downloading "+str(i))
#     for root, subFolders, files in os.walk(srcpath):
#         for file in files:
#             subFolder = os.path.join(path_to_FTP, file[:4], file[4:6])
#             if not os.path.isdir(subFolder):
#                 os.makedirs(subFolder)
#             # print(os.path.join(root, file))
#             # print(subFolder)
#             shutil.copyfile(os.path.join(root, file), os.path.join(subFolder, file))
#             print("Moving "+file)
#     srv.close()

[os.remove(os.path.join(srcpath, f)) for f in os.listdir(srcpath) if f.endswith(".csv")]
# for f in os.listdir(srcpath): if f.endswith(".csv"): os.remove(f)
