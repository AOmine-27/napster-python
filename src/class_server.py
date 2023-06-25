import socket
import multiprocessing
import os
from handle_connection import handle_connection
from db import appendPeerData, searchFile, clearDb, updatePeerData

class Server:
  def __init__(self, ip, port, buffer_size):
    self.ip = ip
    self.port = port
    self.buffer_size = buffer_size
    self.server_socket = socket.socket()

    self.server_socket.bind((self.ip, self.port))
    print(f'Server will be using host {self.ip} and port {self.port}')

  def start(self):
    self.server_socket.listen(5)
    print('Server started...')
    while True:
      client_connection, client_address = self.server_socket.accept()
      print('Connected to', client_address)
      print('Dispatching to new process...')
      process = multiprocessing.Process(target=self.handleConnection, args=(client_connection,))
      process.start()

  def handleConnection(self, connection):
    client_ip = connection.getpeername()[0]
    client_port = connection.getpeername()[1]

    while True:
      try:
        data = connection.recv(self.buffer_size).decode()
        if not data:
          print('No data received, closing connection...')
          connection.close()

        if (data == 'JOIN'):
          self.handleServerJoin(connection, client_ip)

        elif (data == 'SEARCH'):
          self.handleServerSearch(connection)

        elif (data == 'UPDATE'):
          self.handleServerUpdate(connection, client_ip)

      except Exception as e:
        print(f'An error has ocurred, closing connection. Error: {str(e)}')
        connection.close()
        break

  def handleServerJoin(self, connection, client_ip):
    connection.sendall('JOIN_OK'.encode())
    peer_download_port = connection.recv(self.buffer_size).decode()
    data = connection.recv(self.buffer_size).decode()
    if (data == 'NO_FILES'):
      files_array = []
    else:
      files_array = data.split(',')
    appendPeerData(files_array, client_ip, peer_download_port)

    print(f'Files from peer: {data}')

  def handleServerSearch(self, connection):
    connection.sendall('SEARCH_OK'.encode())
    file_name = connection.recv(self.buffer_size).decode()
    peers_with_file_array = searchFile(file_name)
    if (peers_with_file_array == -1):
      connection.sendall(f'No peers with the file {file_name} were found.'.encode())
    else:
      delimiter = "\n"
      files_string = delimiter.join(peers_with_file_array) 
      connection.sendall(files_string.encode())

  def handleServerUpdate(self, connection, client_ip):
    connection.sendall('UPDATE_OK'.encode())
    data = connection.recv(self.buffer_size).decode().split('|',1)
    file_name = data[0]
    peer_download_port = data[1]
    updatePeerData(file_name, client_ip, peer_download_port)


