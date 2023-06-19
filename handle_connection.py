from db import appendPeerData, searchFile, clearDb, updatePeerData
def handle_connection(connection):
  client_ip = connection.getpeername()[0]
  client_port = connection.getpeername()[1]
  print(f'New process created. Connection with [{client_ip}]:[{client_port}]')
  
  while True:
    try:
      data = connection.recv(1024).decode()
      if not data:
        print('No data')
        connection.close()

      if (data == 'JOIN'):
        connection.sendall('JOIN_OK'.encode())

        # Expects array of files from peer
        data = connection.recv(1024).decode()

        # TODO: If peer already on db, updates
        files_array = data.split(",")
        appendPeerData(files_array, client_ip, client_port)

        print(f'Files from peer: {data}')

      elif (data == 'SEARCH'):
        connection.sendall('SEARCH_OK'.encode())
        # Expects an file name to search for
        file_name = connection.recv(1024).decode()
        # TODO: Search for file in db and return list of peers
        print(f'Search for peers with the file {file_name}')
        connection.sendall(f'List of peers with the requested file {file_name}: [...]'.encode())



    except:
      print('Ending connection')
      connection.close()
      break