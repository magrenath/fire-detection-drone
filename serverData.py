import socket                   # Import socket module

port = 60000                    # Reserve a port for your service.
sock = socket.socket()             # Create a socket object          
host = '192.168.1.66'
sock.bind((host, port))            # Bind to the port
sock.listen(1)                     # Now wait for client connection.

# print 'Server listening....'

while True:
    conn, addr = sock.accept()     # Establish connection with client.
    data = conn.recv(1024)

    filename ='sensors.txt'
    f = open(filename,'rb')
    l = f.read(1024)
    while (l):
       conn.send(l)
       l = f.read(1024)
    f.close()
    # conn.close()











