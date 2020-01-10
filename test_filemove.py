import os
import shutil

srcpath = "/mnt/c/Users/WMINSKEY/.pen/ftp-file-practice/input/"
destpath = "/mnt/c/Users/WMINSKEY/.pen/ftp-file-practice/output/"

# sorts files of YYYYMMDD format to Y and M folder subsystems
for root, subFolders, files in os.walk(srcpath):
    for file in files:
        subFolder = os.path.join(destpath, file[:4], file[4:6])
        if not os.path.isdir(subFolder):
            os.makedirs(subFolder)
        if os.path.exists(os.path.join(subFolder, file)):
            if (int(os.stat(os.path.join(root, file)).st_size) - int(os.stat(os.path.join(subFolder, file)).st_size)) > 0:
                shutil.copy2(os.path.join(root, file), subFolder)
        else:
            shutil.copy2(os.path.join(root, file), subFolder)
