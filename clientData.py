import socket                   # Import socket module
import time

s = socket.socket()             # Create a socket object
host = '192.168.1.66'
port = 60000                    # Reserve a port for your service.

s.connect((host, port))
s.send("Hello server!").encode

with open('received_file', 'wb') as f:
    
    while True:
        try:
            data = s.recv(1024).encode
            print('data=%s', (data))
        finally:
            f.close()
            s.close()