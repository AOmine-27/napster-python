import os
# the name of file we want to send, make sure it exists
filename = "poc-multiprocess.py"
# get the file size
filesize = os.path.getsize(filename)
print(os.path.getsize(os.getcwd()+'/'+filename))