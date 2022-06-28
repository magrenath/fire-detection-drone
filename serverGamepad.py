import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.1.66', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    print('Drone availiable, waiting connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        while True:
            data1 = connection.recv(5000)
            print(data1.decode())
    finally:
        connection.close()