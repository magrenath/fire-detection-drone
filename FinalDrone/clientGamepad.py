import socket
import pygame
import time
import numpy


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('172.20.10.4', 10000)
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
    startdrone = joystick.get_button(0)
    stopdrone = joystick.get_button(3)
    throttle = round(numpy.interp(T, [-1, 1], [100, 0]))
    yaw = round(numpy.interp(Y, [-1, 1], [-100, 100]))
    pitch = round(numpy.interp(P, [-1, 1], [100, -100]))
    roll = round(numpy.interp(R, [-1, 1], [-100, 100]))
    pygame.event.pump()

    message_FromGamepad = str(str(throttle) + ',' + str(yaw) + ',' + str(pitch) + ',' + str(roll) + ',' + str(startdrone) + ',' + str(stopdrone))
    print(message_FromGamepad)

    # -------------------------------------
    # SendData
    # -------------------------------------

    sock.send(message_FromGamepad.encode())
    time.sleep(0.5)