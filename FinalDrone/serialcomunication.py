import serial
#from serverGamepad import stringCommands
# create serial connection
if __name__ == '_main_':
    ser= serial.Serial('/dev/ttyUSB0',9600,timeout=1)
    ser.flush()

    while True:
        if ser.in_waiting>0:
            # read sensor data
            sensor_data= ser.readline().decode('utf-8').rstrip()
            print(sensor_data)

            #send gamepad commands
            file=open('sensores.txt','r')
            pwm=file.read()
            ser.write((pwm).encode().rstrip())
