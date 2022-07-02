import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('172.20.10.4', 10000)
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
            #sock.send(sensor_data)
            message_FromGamepad = connection.recv(5000)
            stringCommands = (message_FromGamepad.decode('utf-8'))
            print(stringCommands)
            file=open('sensores.txt','w')
            file.write(stringCommands)
            #file.close()
    finally:
        connection.close()