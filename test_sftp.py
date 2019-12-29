# -*- coding: utf-8 -*-
"""
2019
@author: wuffalo
"""
import pysftp
import config_sftp
import pandas as pd
import os

# Make sure known hosts file has correct permissions
# chmod 644 ~/.ssh/known_hosts
# chmod 700 ~/.ssh
cnopts = pysftp.CnOpts()
cnopts.hostkeys.load(config_sftp.host_file)

stfp_host = config_sftp.host
sftp_name = config_sftp.username
sftp_port = config_sftp.port
sftp_pw = config_sftp.password

# stfp_host = host
# sftp_name = username
# sftp_port = port
# sftp_pw = password

srv = pysftp.Connection(host=stfp_host,username=sftp_name,password=sftp_pw,cnopts=cnopts)

data = srv.listdir()

remote = srv.chdir('.')

print(srv.getcwd())
print(os.path.abspath(srv.getcwd()))

print("Check if file exists: ")
if srv.exists('/.csv') == True:
    print("Yes")

srv.close()

df_ftx = []

df_ftx = data

print(data[0],data[1],data[-1])

d1 = df_ftx.index('20191222.csv')

print(d1)
print(df_ftx[d1])

# list comprehension, enumate over a list looking for indexes of j instances
# [i for i, j in enumerate(['foo', 'bar', 'baz']) if j == 'bar']
d5 = [i for i, j in enumerate(df_ftx) if j == '20191222.csv']

print(type(d5))
print(d5[0])
