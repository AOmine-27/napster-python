import socket
import os
import multiprocessing

class DownloadService:
  def __init__(self, ip, download_port, folder_path, buffer_size):
    self.ip = ip
    self.download_port = download_port
    self.folder_path = folder_path
    self.buffer_size = buffer_size

    self.download_socket = socket.socket()
    self.download_socket.bind((self.ip, self.download_port))
    print(f'Download peer service listening at {self.ip}:{self.download_port}')

  def start(self): 
    self.download_socket.listen(5)
    while True:
      client_connection, client_address = self.download_socket.accept()
      self.new_download_process = multiprocessing.Process(target=self.handleDownloadRequest, args=(client_connection,))
      print('New process for download requests')
      self.new_download_process.start()

  def handleDownloadRequest(self, connection):
    client_ip = connection.getpeername()[0]
    client_port = connection.getpeername()[1]

    data = connection.recv(self.buffer_size).decode()
    if (data == 'DOWNLOAD_REQUEST'):
      connection.sendall('DOWNLOAD_OK'.encode())

      # Expects a filename
      file_name = connection.recv(self.buffer_size).decode()

      files = os.listdir(os.getcwd()+ self.folder_path)
      if file_name in files:
        connection.sendall('FILE_OK'.encode())
        self.sendFile(file_name,connection)
        print('sent a file')
      else:
        connection.send('FILE_NOT_OK'.encode())
        connection.close()
    else:
      print(data)
      connection.close()
    return

  def sendFile(self, file_name, connection):
    files = os.listdir(os.getcwd() + self.folder_path)
    if file_name in files:
      full_file_path = os.getcwd() + self.folder_path + '/' + file_name

      file_size = os.path.getsize(full_file_path)
      connection.send(str(file_size).encode())

      file = open(full_file_path, 'rb')
      data = file.read(self.buffer_size)

      while data:
        connection.sendall(data)
        data = file.read(self.buffer_size)
      connection.close()

  def finishService(self):
    self.download_socket.close()