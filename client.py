import socket
import os
from menu import printMenu, executeCommand
from peer_download_service import peerDownloadService
import multiprocessing
import json

PEER_IP = '127.0.0.1'
PEER_PORT = 8000
PEER_DOWNLOAD_PORT = 9000
SERVER_IP = '127.0.0.1'
SERVER_PORT = 1099
BUFFER_SIZE = 1024

def client():
  print(PEER_IP)
  process = multiprocessing.Process(target=peerDownloadService, args=(PEER_IP,PEER_DOWNLOAD_PORT,input_folderpath))
  process.start()

  client_socket = socket.socket()
  print(f'Bind host {PEER_IP} and port {PEER_PORT}')
  client_socket.bind((PEER_IP, int(PEER_PORT)))

  client_socket.connect((SERVER_IP, SERVER_PORT))
  print(f'Connected to server on {SERVER_IP} and port {SERVER_PORT}')

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
            outbound_port = input('Input new outbound port: ')
            target_peer_ip = input('Input target peer ip: ')
            target_peer_port = input('Input target peer port: ')

            request_download_socket = socket.socket()
            request_download_socket.bind((PEER_IP, int(outbound_port)))
            request_download_socket.connect((target_peer_ip, int(target_peer_port)))
            request_download_socket.sendall("DOWNLOAD_REQUEST".encode())

            response = request_download_socket.recv(BUFFER_SIZE).decode()

            if (response == 'DOWNLOAD_OK'):
              request_file = input('Input the requested file name: ')
              request_download_socket.sendall(request_file.encode())

              request_file_path = os.getcwd() + input_folderpath + '/' + request_file
              with open(request_file_path, 'wb') as file:
                bytes_read = request_download_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                  break
                file.write(bytes_read)
              print('Download finished')
              request_download_socket.close()
              

          elif (command == 'QUIT'):
            print("Closing connection")
            client_socket.shutdown(socket.SHUT_RDWR)
            client_socket.close()
            break
          else:
            client_socket.sendall(command.encode())
      
      except client_socket.error:
          break

  # Close the client socket
  client_socket.close()

if __name__ == '__main__':
  # Prompt peer info
  if not (input_peer_ip := input('Input peer IP (default 127.0.0.1): ')):
    print('Setting ip to default 127.0.0.1')
    print(f'aa{PEER_IP}')
  else:
    print(f'Setting ip to {input_peer_ip}')
    PEER_IP = input_peer_ip

  if not (input_peer_port := input('Input peer port (default 8000): ')):
    print('Setting port to default 8000')
  else:
    PEER_PORT = input_peer_port

  if not (input_peer_download_port := input('Input peer download port (default 9000): ')):
    print('Setting port to default 9000')
  else:
    PEER_DOWNLOAD_PORT = input_peer_download_port

  input_folderpath = input('Input folder path (ex. /Documents):')
  client()