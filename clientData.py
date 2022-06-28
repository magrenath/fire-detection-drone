
import socket                   # Import socket module
import time

s = socket.socket()             # Create a socket object
host = '192.168.1.66'
port = 60000                    # Reserve a port for your service.

s.connect((host, port))
s.send(("Hello server!").encode())

try:
    data = s.recv(1024)
    print(data.decode())
finally:
    #f.close()
    s.close()