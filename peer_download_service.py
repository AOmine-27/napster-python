import socket
import multiprocessing
import os

BUFFER_SIZE = 1024

def sendFile(file_name, peer_folder, connection):
  files = os.listdir(os.getcwd()+peer_folder)
  if file_name in files:
    full_file_path = os.getcwd() + peer_folder + '/' + file_name
    # file_size = os.path.getsize(full_file_path)
    # connection.send(file_size.encode())

    with open(full_file_path, 'rb') as file:
      bytes_read = file.read(BUFFER_SIZE)
      if bytes_read:
        connection.sendall(bytes_read)


def handleDownloadRequest(connection, folder_path):
  client_ip = connection.getpeername()[0]
  client_port = connection.getpeername()[1]
  # print(f'New process created. Connection with [{client_ip}]:[{client_port}]')

  data = connection.recv(1024).decode()
  if (data == 'DOWNLOAD_REQUEST'):
    connection.sendall('DOWNLOAD_OK'.encode())

    # Expects a filename
    file_name = connection.recv(1024).decode()

    sendFile(file_name,folder_path,connection)

    connection.close()
  else:
    connection.close()
  return


def peerDownloadService(ip, port, folder_path):
  # print('Download peer service is starting')
  download_socket = socket.socket()
  download_socket.bind((ip,int(port)))
  download_socket.listen(5)
  print(f'Download peer service listening at {ip}:{port}')

  while True:
    client_connection, client_address = download_socket.accept()
    # print(f'Received connection from {client_address}')
    # print('Dispatching to new process...')
    process = multiprocessing.Process(target=handleDownloadRequest, args=(client_connection,folder_path,))
    process.start()