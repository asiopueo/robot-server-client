#!/usr/bin/env python

import sys
from socket import *
from time import ctime          # Import necessary modules

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

    while True:
        data = ''
        data = tcpCliSock.recv(BUFSIZ).decode()    # Receive and decode data sent from the client.
        # Analyze the command received and control the car accordingly.
        if not data:
            break
        if data == ctrl_cmd[0]:
            print('Motor moving forward')
            motor.forward()
        elif data == ctrl_cmd[1]:
            print('Received backward cmd')
            motor.backward()
        elif data == ctrl_cmd[2]:
            print('Received left cmd')
            motor.left()
        elif data == ctrl_cmd[3]:
            print('Received right cmd')
            motor.right()
        elif data == ctrl_cmd[4]:
            print('Received stop cmd')
            motor.stop()
        elif data == ctrl_cmd[5]:
            print('read cpu temp...')
            temp = cpu_temp.read()
            tcpCliSock.send('[%s] %0.2f' % (ctime(), temp))
        elif data == ctrl_cmd[8]:
            print('Received x+ cmd')
            pantilt.move_increase_x()
        elif data == ctrl_cmd[9]:
            print('Received x- cmd')
            pantilt.move_decrease_x()
        elif data == ctrl_cmd[10]:
            print('Received y+ cmd')
            pantilt.move_increase_y()
        elif data == ctrl_cmd[11]:
            print('Received y- cmd')
            pantilt.move_decrease_y()
        elif data == ctrl_cmd[12]:
            print('home_x_y')
            pantilt.home_x_y()
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

        elif data[0:5] == 'turn=':    #Turning Angle
            print('data =', data)
            angle = data.split('=')[1]
            try:
                angle = int(angle)
                #car_dir.turn(angle)
            except:
                print('Error: angle =', angle)

        elif data[0:8] == 'forward=':
            print('data =', data)
            spd = data[8:]
            try:
                spd = int(spd)
                #motor.forward(spd)
            except:
                print('Error speed =', spd)

        elif data[0:9] == 'backward=':
            #print("data =", data)
            spd = data.split('=')[1]
            try:
                spd = int(spd)
                #motor.backward(spd)
            except:
                print('ERROR, speed =', spd)
        else:
                print('Command Error! Cannot recognize command: ', data)

tcpSerSock.close()
