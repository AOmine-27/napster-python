import socket
import os
from menu import printMenu, executeCommand
import json

PEER_IP = '127.0.0.1'
PEER_PORT = 8000
SERVER_IP = '127.0.0.1'
SERVER_PORT = 1099
BUFFER_SIZE = 1024

# Prompt peer info
if not (input_peer_ip := input('Input peer IP (default 127.0.0.1): ')):
  print('Setting ip to default 127.0.0.1')
else:
  print(f'Setting ip to {input_peer_ip}')
  PEER_IP = input_peer_ip

if not (input_peer_port := input('Input peer port (default 8000): ')):
  print('Setting port to default 8000')
else:
  PEER_PORT = input_peer_port

input_folderpath = input('Input folder path (ex. /Documents):')


client_socket = socket.socket()
print(f'Bind host {PEER_IP} and port {PEER_PORT}')
client_socket.bind((PEER_IP, int(PEER_PORT)))


client_socket.connect((SERVER_IP, SERVER_PORT))
print(f'Connected to server on {SERVER_IP} and port {SERVER_PORT}')

print('Connected to the server.')

while True:
    try:
        printMenu()
        arg = input()
        command = executeCommand(arg)
        if (command == 'JOIN'):
          client_socket.sendall(command.encode())
          response = client_socket.recv(BUFFER_SIZE).decode()

          # Expects JOIN_OK from server
          if (response == 'JOIN_OK'):
            file_full_path = os.getcwd() + input_folderpath
            files = os.listdir(file_full_path)
            print(f'Sou peer [{PEER_IP}]:[{PEER_PORT}] com os arquivos{files}')
            
            delimiter = ","
            files_string= delimiter.join(files)
            client_socket.sendall(files_string.encode())
        elif (command == 'SEARCH'):
          client_socket.sendall(command.encode())
          response = client_socket.recv(BUFFER_SIZE).decode()
          if (response == 'SEARCH_OK'):
            search_file = input('Input the file to search: ')
            client_socket.sendall(search_file.encode())
            # Expects a list of peers with the file
            response = client_socket.recv(BUFFER_SIZE).decode()
            print(response)
        elif (command == 'DOWNLOAD'):
          target_peer_ip = input('Input target peer ip: ')
          target_peer_port = input('Input target peer port: ')
          client_socket.connect((target_peer_ip,target_peer_port))
          print(f'Connected to port on {target_peer_ip} and port {target_peer_port}')

        elif (command == 'QUIT'):
          print("Closing connection")
          client_socket.shutdown(socket.SHUT_RDWR)
          client_socket.close()
          break
        else:
          client_socket.sendall(command.encode())

        if not response:
            break
      
    
    except client_socket.error:
        break

# Close the client socket
client_socket.close()
