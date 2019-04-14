#!/usr/bin/env python

import sys
from socket import *
from time import ctime, sleep

import fake_rpi.RPi
sys.modules['RPi'] = fake_rpi.RPi     # Mock RPi (GPIO)
sys.modules['smbus'] = fake_rpi.smbus # Mock smbus (I2C)

#import RPi.GPIO as GPIO
#from fake_rpi.RPi import GPIO

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



def getCommand(data):
    try:
        command, arg = data.split('=')
    except:
        command = data, arg = None

    # Motor commands
    if command == ctrl_cmd[0]:
        print('Received forward cmd')
        return command, arg
    elif command == ctrl_cmd[1]:
        print('Received backward cmd')
        return command, arg
    elif command == ctrl_cmd[2]:
        print('Received left cmd')
        return command, arg
    elif command == ctrl_cmd[3]:
        print('Received right cmd')
        return command, arg
    elif command == ctrl_cmd[4]:
        print('Received stop cmd')
        return command, arg


    # CPU readouts
    elif data == ctrl_cmd[5]:
        print('read cpu temp...')
        temp = cpu_temp.read()
        tcpCliSock.send('[%s] %0.2f' % (ctime(), temp))


    # Camera mount
    elif command == ctrl_cmd[8]:
        print('Received x+ cmd')
        return command, arg
    elif command == ctrl_cmd[9]:
        print('Received x- cmd')
        return command, arg
    elif command == ctrl_cmd[10]:
        print('Received y+ cmd')
        return command, arg
    elif command == ctrl_cmd[11]:
        print('Received y- cmd')
        return command, arg
    elif command == ctrl_cmd[12]:
        print('Received home_x_y cmd')
        return command, arg

    # Change speed
    elif data[0:5] == 'speed':
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

    #Turning Angle
    elif data[0:5] == 'turn=':
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








class MotorStateMachine:
    def __init__(self):
        self.state = 'HALT'

    def set_state(self, new_state, arg=None):
        self.state = new_state
        self.parameter = arg
        self.timer = 0

    def run(self):
        if self.state == 'forward':
            if self.parameter:
                duration = int(self.parameter)
                self.timer += duration
                motor.forward()
                sleep(duration)
                motor.stop()
            else:
                motor.forward()
        elif self.state == 'backward':
            if self.parameter:
                duration = int(self.parameter)
                motor.backward()
                sleep(duration)
                motor.stop()
        elif self.state == 'left':
            if self.parameter:
                duration = int(self.parameter)
                motor.left()
                sleep(duration)
                motor.stop()
            else:
                motor.left()
        elif self.state == 'right':
            if self.parameter:
                duration = int(self.parameter)
                motor.right()
                sleep(duration)
                motor.stop()
            else:
                motor.right()
        elif self.state == 'halt':
            motor.stop()



class MountStateMachine:
    def __init__(self):
        self.state = 'home_x_y'

    def set_state(self, new_state):
        self.state = new_state

    def run(self):
        if self.state == ctrl_cmd[8]:
            if self.parameter:
                pantilt.move_increase_x(self.parameter)
            else:
                pantilt.move_increase_x(self.parameter)
        elif self.state == ctrl_cmd[9]:
            if self.parameter:
                pantilt.move_decrease_x(self.parameter)
            else:
                pantilt.move_decrease_x(self.parameter)
        elif self.state == ctrl_cmd[10]:
            if self.parameter:
                pantilt.move_increase_y(self.parameter)
            else:
                pantilt.move_increase_y(self.parameter)
        elif self.state == ctrl_cmd[11]:
            if self.parameter:
                pantilt.move_decrease_y(self.parameter)
            else:
                pantilt.move_decrease_y(self.parameter)
        elif self.state == ctrl_cmd[12]:
            pantilt.home_x_y()




if __name__=='__main__':
    # Initializing state machines:
    motor_sm = MotorStateMachine()
    mount_sm = MountStateMachine()

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
            if not data:
                break

            # Analyze the command received and control the car accordingly.
            command, arg = getCommand(data)

            motor_sm.set_state(command, arg)
            motor_sm.run()

            #mount_sm.set_state(state)
            #mount_sm.run()



tcpSerSock.close()
