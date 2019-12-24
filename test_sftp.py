# -*- coding: utf-8 -*-
"""
2019
@author: wuffalo
"""
import pysftp
import config_sftp

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

srv.close()

for i in data:
    print(i)

# srv.close()