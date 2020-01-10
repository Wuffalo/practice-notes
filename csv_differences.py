# -*- coding: utf-8 -*-
"""
2020
@author: wuffalo
"""

local = "/mnt/shared-drive/05 - Office/FTP/FTP Files/2018/08/20180818.csv"
remote = "/mnt/shared-drive/05 - Office/FTP/FTP Files/2018/20180818.csv"
output = "/mnt/c/Users/WMINSKEY/.pen/ftp-file-practice/update.csv"

with open(local, 'r') as t1, open(remote, 'r') as t2:
    fileone = t1.readlines()
    filetwo = t2.readlines()

with open(output, 'w') as outFile:
    for line in filetwo:
        if line not in fileone:
            outFile.write(line)
