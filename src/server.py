from class_server import Server

SERVER_IP = '127.0.0.1'
SERVER_PORT = 1099
BUFFER_SIZE = 4096

if __name__ == '__main__':
  server = Server(SERVER_IP, SERVER_PORT, BUFFER_SIZE)
  server.start()