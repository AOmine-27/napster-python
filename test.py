import os
folder_full_path = os.getcwd() + '/peerX'
files = os.listdir(folder_full_path)
print('Files: ', end=' ')
for file in files:
    print(file, end=' ')
print()