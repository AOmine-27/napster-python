from class_client import Client

PEER_IP = '127.0.0.1'
PEER_PORT = 8000
PEER_DOWNLOAD_PORT = 9000
SERVER_IP = '127.0.0.1'
SERVER_PORT = 1099
BUFFER_SIZE = 4096

if __name__ == '__main__':
  if not (input_peer_ip := input('Input peer IP (default 127.0.0.1): ')):
    print('Setting ip to default 127.0.0.1')
  else:
    PEER_IP = input_peer_ip

  if not (input_peer_port := input('Input peer port (default 8000): ')):
    print('Setting port to default 8000')
  else:
    PEER_PORT = input_peer_port

  if not (input_peer_download_port := input('Input peer download port (default 9000): ')):
    print('Setting port to default 9000')
  else:
    PEER_DOWNLOAD_PORT = input_peer_download_port

  folder_path = input('Input folder path (ex. /Documents):')

  client = Client(PEER_IP, int(PEER_PORT), int(PEER_DOWNLOAD_PORT), int(BUFFER_SIZE), folder_path)
  client.connectToServer()
  client.startDownloadService()
  client.start()