

import socket
import keyboard

HOST = "172.20.10.5"  # The server's hostname or IP address
PORT = 65432  # The port used by the server        

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST,PORT))

def getKeyPressed():
    command = 'NOT'
    if(keyboard.is_pressed('w')):
        command = 'THROTTLE +'
    elif(keyboard.is_pressed('s')):
        command = 'THROTTLE -'
    elif(keyboard.is_pressed('d')):
        command = 'YAW +'
    elif(keyboard.is_pressed('a')):
        command = 'YAW -'
    elif(keyboard.is_pressed('i')):
        command = 'PITCH +'
    elif(keyboard.is_pressed('k')):
        command = 'PITCH -'
    elif(keyboard.is_pressed('l')):
        command = 'ROLL +'
    elif(keyboard.is_pressed('j')):
        command = 'ROLL -'
    elif(keyboard.is_pressed('q')):
        command = 'QUIT'

    return command

while True:

    command= getKeyPressed()
    conv = bytes(command,'ascii')
    client.send(conv)

    reply = client.recv(1024)

    if(reply == b'quit'):
        break
    print(reply)