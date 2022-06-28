import socket
import pygame
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.1.66', 10000)
print('Connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

# -----------------------------------------
# Command Initialization
# -----------------------------------------
pygame.init()
pygame.joystick.init()

# Get count of joysticks.
joystick_count = pygame.joystick.get_count()
print('Found ' + str(joystick_count) + ' joystick.')

# init joystick
joystick = pygame.joystick.Joystick(0)  # Assuming we have only one
joystick.init()

# Get the name from the OS for the controller/joystick.
joystick_name = joystick.get_name()
print('Connected to ' + joystick_name)

# -----------------------------------------
# GetData
# -----------------------------------------

while True:

    Y = round(joystick.get_axis(0) * 100)/100
    T = round(-joystick.get_axis(1) * 100)/100
    P = round(-joystick.get_axis(3) * 100)/100
    R = round(joystick.get_axis(2) * 100)/100
    A = joystick.get_button(0)
    pygame.event.pump()

    message = str('Y ' + str(Y) + '; T ' + str(T) + '; R ' + str(R) + '; P ' + str(P) + '; A ' + str(A))
    print(message)

    # -------------------------------------
    # SendData
    # -------------------------------------

    sock.send(message.encode())

    time.sleep(0.5)