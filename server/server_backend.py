#!/usr/bin/env python

import sys
from socket import *
from time import ctime, sleep

import RPi.GPIO as GPIO
import pantilt
import car_dir
import motor


ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']

busnum = 1          # Edit busnum to 0, if you uses Raspberry Pi 1 or 0

HOST = ''           # The variable of HOST is null, so the function bind( ) can be bound to all valid addresses.
PORT = 21567
BUFSIZ = 1024       # Size of the buffer
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)    # Create a socket.
tcpSerSock.settimeout(30)
tcpSerSock.bind(ADDR)    # Bind the IP address and port number of the server.
tcpSerSock.listen(5)


pantilt.setup(busnum=busnum)
car_dir.setup(busnum=busnum)
motor.setup(busnum=busnum)     # Initialize the Raspberry Pi GPIO connected to the DC motor.
pantilt.home_x_y()
car_dir.home()


while True:
    print('Waiting for connection...')
    # Waiting for connection. Once receiving a connection, the function accept() returns a separate
    # client socket for the subsequent communication. By default, the function accept() is a blocking
    # one, which means it is suspended before the connection comes.
    try:
        tcpCliSock, addr = tcpSerSock.accept()
    except:
        print("TCP-server timed out - no connection established.")
        sys.exit()

    print('...connected from :', addr)     # Print the IP address of the client connected with the server.

    # Main loop
    while True:
        data = ''
        data = tcpCliSock.recv(BUFSIZ).decode()    # Receive and decode data sent from the client.
        # Analyze the command received and control the car accordingly.
        if not data:
            break


        ####################
        # Locomotion control
        ####################

        if data == ctrl_cmd[0]:
            print('Motor moving forward')
            motor.forward()
        elif data[0:8] == 'forward=':
            print('data =', data)
            duration = data[8:]
            try:
                duration = int(duration)
                motor.forward()
                sleep(duration)
                motor.stop()
            except:
                print('Error duration =', duration)

        elif data == ctrl_cmd[1]:
            print('Received backward cmd')
            motor.backward()
        elif data[0:9] == 'backward=':
            print("data =", data)
            duration = data.split('=')[1]
            try:
                duration = int(duration)
                motor.backward()
                sleep(duration)
                motor.stop()
            except:
                print('ERROR, duration =', duration)

        elif data == ctrl_cmd[2]:
            print('Received left cmd')
            motor.left()
        elif data[0:5] == 'left=':    #Turning Angle
            print('data =', data)
            duration = data.split('=')[1]
            try:
                duration = int(duration)
                motor.left()
                sleep(duration)
                motor.stop()
            except:
                print('Error: duration =', duration)

        elif data == ctrl_cmd[3]:
            print('Received right cmd')
            motor.right()
        elif data[0:6] == 'right=':
            print('data =', data)
            duration = data.split('=')[1]
            try:
                duration = int(duration)
                motor.right()
                sleep(duration)
                motor.stop()
            except:
                print('Error: duration =', duration)


        elif data == ctrl_cmd[4]:
            print('Received stop cmd')
            motor.stop()


        elif data == ctrl_cmd[5]:
            print('read cpu temp...')
            temp = cpu_temp.read()
            tcpCliSock.send('[%s] %0.2f' % (ctime(), temp))


        ####################
        # Pan/tilt-control
        ####################
        elif data == ctrl_cmd[8]:
            print('Received x+ cmd')
            pantilt.move_increase_x()
        elif data[0:3] == 'x+=':
            print('data =', data)
            angle = data[3:]
            try:
                angle = int(angle)
                pantilt.move_increase_x()
            except:
                print('Error angle =', angle)

        elif data == ctrl_cmd[9]:
            print('Received x- cmd')
            pantilt.move_decrease_x()
        elif data[0:3] == 'x-=':
            print('angle =', angle)
            angle = data[3:]
            try:
                angle = int(angle)
                pantilt.move_decrease_x()
            except:
                print('Error angle =', angle)

        elif data == ctrl_cmd[10]:
            print('Received y+ cmd')
            pantilt.move_increase_y()
        elif data[0:3] == 'y+=':
            print('data =', data)
            duration = data[3:]
            try:
                angle = int(angle)
                pantilt.move_increase_y()
            except:
                print('Error angle =', angle)

        elif data == ctrl_cmd[11]:
            print('Received y- cmd')
            pantilt.move_decrease_y()
        elif data[0:3] == 'y-=':
            print('data =', data)
            angle = data[3:]
            try:
                angle = int(angle)
                pantilt.move_decrease_y()
            except:
                print('Error angle =', angle)

        elif data == ctrl_cmd[12]:
            print('home_x_y')
            pantilt.home_x_y()
        else:
            print('Command Error! Cannot recognize command: ', data)


        """
        elif data[0:5] == 'speed':     # Change the speed
            print(data)
            numLen = len(data) - len('speed')
            if numLen == 1 or numLen == 2 or numLen == 3:
                tmp = data[-numLen:]
                print('tmp(str) = %s' % tmp)
                spd = int(tmp)
                print('spd(int) = %d' % spd)
                if spd < 24:
                    spd = 24
                #motor.setSpeed(spd)
        """

tcpSerSock.close()
