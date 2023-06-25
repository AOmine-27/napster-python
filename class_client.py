import socket
import os
import multiprocessing
from class_client_download import DownloadService
from menu import printMenu, executeCommand

SERVER_IP = '127.0.0.1'
SERVER_PORT = 1099

class Client:
  def __init__(self, ip, port, download_port, buffer_size, folder_path):
    self.ip = ip
    self.port = port
    self.download_port = download_port
    self.buffer_size = buffer_size
    self.folder_path = folder_path
    self.client_socket = socket.socket()
    self.client_socket.bind((ip, port))

  def connectToServer(self):
    self.client_socket.connect((SERVER_IP, SERVER_PORT))
    print(f'Connected to server on {SERVER_IP} and port {SERVER_PORT}')

  def startDownloadService(self):
    self.download_service = DownloadService(self.ip, self.download_port, self.folder_path, self.buffer_size)
    self.download_process = multiprocessing.Process(target=self.download_service.start, args=())
    self.download_process.start()
  
  def handleJoin(self):
    self.client_socket.sendall('JOIN'.encode())
    response = self.client_socket.recv(self.buffer_size).decode()

    if (response == 'JOIN_OK'):
      self.client_socket.sendall(str(self.download_port).encode())
      folder_full_path = os.getcwd() + self.folder_path
      files = os.listdir(folder_full_path)
      if not files:
        print(f'Sou peer {self.ip}:{self.download_port} com nenhum arquivo')
        self.client_socket.sendall('NO_FILES'.encode())
      else:
        print(f'Sou peer {self.ip}:{self.download_port} com os arquivos', end=' ')
        for file in files:
          print(file, end=' ')
        print()
        
        delimiter = ","
        files_string= delimiter.join(files)
        self.client_socket.sendall(files_string.encode())

  def handleSearch(self):
    self.client_socket.sendall('SEARCH'.encode())
    response = self.client_socket.recv(self.buffer_size).decode()

    if (response == 'SEARCH_OK'):
      self.search_file = input('Input the file to search: ')
      data = self.search_file + '|' + str(self.download_port)
      self.client_socket.sendall(data.encode())
      
      # Expects a list of peers with the file
      response = self.client_socket.recv(self.buffer_size).decode()
      print(response)

  def sendUpdate(self, file_name):
    self.client_socket.sendall('UPDATE'.encode())
    response = self.client_socket.recv(self.buffer_size).decode()
    if (response == 'UPDATE_OK'):
      data = file_name + '|' + str(self.download_port)
      self.client_socket.sendall(data.encode())

  def handleDownload(self):
    outbound_port = input('Input new outbound port: ')
    target_peer_ip = input('Input target peer ip: ')
    target_peer_port = input('Input target peer port: ')

    print('Start download request')
    request_download_socket = socket.socket()
    request_download_socket.bind((self.ip, int(outbound_port)))
    request_download_socket.connect((target_peer_ip, int(target_peer_port)))
    request_download_socket.sendall("DOWNLOAD_REQUEST".encode())

    response = request_download_socket.recv(self.buffer_size).decode()

    if (response == 'DOWNLOAD_OK'):
      # request_file = input('Input the requested file name: ')
      request_file = self.search_file
      request_download_socket.sendall(request_file.encode())
      response = request_download_socket.recv(self.buffer_size).decode()
      if (response == 'FILE_OK'):
        request_file_path = os.getcwd() + self.folder_path + '/' + request_file

        file_size = int(request_download_socket.recv(self.buffer_size).decode())

        file = open(request_file_path, 'wb')
        data = request_download_socket.recv(self.buffer_size)
        downloaded_file_size = os.path.getsize(request_file_path)

        while len(data) > 0:
          file.write(data)
          downloaded_file_size = os.path.getsize(request_file_path)
          print(str(downloaded_file_size/1024) + 'KB / '+str(file_size/1024)+' KB downloaded!', end='\r')
          print()
          if (len(data) < self.buffer_size): 
            file.close()
            break
          data = request_download_socket.recv(self.buffer_size)
        print(f'Arquivo {request_file} baixado com sucesso na pasta {self.folder_path}')
        
        request_download_socket.close()
        self.sendUpdate(request_file)
      else:
        print('Error occured. Peer does not have the file anymore')

  def start(self):
    while True:
      try:
        printMenu()
        arg = input()
        command = executeCommand(arg)

        if (command == 'JOIN'):
          self.handleJoin()

        elif (command == 'SEARCH'):
          self.handleSearch()
        
        elif (command == 'DOWNLOAD'):
          self.handleDownload()

        elif (command == 'QUIT'):
          self.client_socket.close()
          self.download_service.finishService()
          self.download_process.terminate()
          break

      except Exception as e:
        print(str(e))
        self.client_socket.close()
        break