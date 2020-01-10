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

dfl = df_local['day_file']
dfr = df_remote['day_file']

df_out = dfr[~dfr.isin(dfl)].dropna()

if df_out.empty == True:
    srv.close()
    print("Nothing to update.")
    print(df_local['day_file'].tail(1))
    print(df_remote['day_file'].tail(1))
else:
    for i in df_out:
        j = (str(i)+'.csv')
        srv.get(j, '/mnt/c/Users/WMINSKEY/.pen/ftp-file-practice/downloaded/'+j)
        print("Downloading "+str(i))
    for root, subFolders, files in os.walk(srcpath):
        for file in files:
            subFolder = os.path.join(path_to_FTP, file[:4], file[4:6])
            if not os.path.isdir(subFolder):
                os.makedirs(subFolder)
            # print(os.path.join(root, file))
            # print(subFolder)
            shutil.copyfile(os.path.join(root, file), os.path.join(subFolder, file))
            print("Moving "+file)
    srv.close()

[os.remove(os.path.join(srcpath, f)) for f in os.listdir(srcpath) if f.endswith(".csv")]
# for f in os.listdir(srcpath): if f.endswith(".csv"): os.remove(f)
