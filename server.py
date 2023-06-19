import socket
import multiprocessing
import os
from handle_connection import handle_connection

HOST = '127.0.0.1'  # Server IP address
PORT = 1099       # Server port
BUFFER_SIZE = 1024

def server():
    print('Input server host (default 127.0.0.1) : ')
    input_host = input()

    print('Input server port (default 1099) : ')
    input_port = input()
    
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket = socket.socket()
    if (input_host != '' and input_port != ''):
        server_socket.bind((input_host, int(input_port)))
        print(f'Using host {input_host} and port {input_port}')
    else:
        server_socket.bind((HOST, PORT))
        print(f'Using host {HOST} and port {PORT}')

    server_socket.listen(5)

    while True:
        client_connection, client_address = server_socket.accept()
        print('Connected to', client_address)
        print('Dispatching to new process...')
        process = multiprocessing.Process(target=handle_connection, args=(client_connection,))
        process.start()


if __name__ == '__main__':
    server()
