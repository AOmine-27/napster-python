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

        peers_with_file_array = searchFile(file_name)
        if (peers_with_file_array == -1):
          connection.sendall(f'No peers with the file {file_name} were found.'.encode())
        else:
          delimiter = "\n"
          files_string = delimiter.join(peers_with_file_array) 
          connection.sendall(files_string.encode())

    except:
      print('Ending connection')
      connection.close()
      break