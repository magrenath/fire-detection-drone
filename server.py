import socket

HOST = "172.20.10.5"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)         

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind((HOST,PORT))
except socket.error:
    print('Bind failed')


server.listen(1)
print('Drone on. Waiting commands')

(conn, addr) = server.accept()

print(f'Connected with: {addr}')

while True:
    data = conn.recv(1024)
    reply= "No commands"

    if(data != b'NOT'):
        print(data)
        reply = 'OK'
    if(data == b'QUIT'):
        conn.send(bytes('Quit','utf-8'))
        break
    
    conv = bytes(reply,'utf-8')
    conn.send(conv)

conn.close()
