#!/usr/bin/env python

import sys
from socket import *
from time import ctime, sleep
from time import time as time

import fake_rpi.RPi
sys.modules['RPi'] = fake_rpi.RPi     # Mock RPi (GPIO)
sys.modules['smbus'] = fake_rpi.smbus # Mock smbus (I2C)


fake_rpi.toggle_print(False)

#import RPi.GPIO as GPIO
#from fake_rpi.RPi import GPIO

import pantilt
import car_dir
import motor
import pid


import threading
import serial

ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']

busnum = 1          # Edit busnum to 0, if you uses Raspberry Pi 1 or 0

HOST = ''           # The variable of HOST is null, so the function bind( ) can be bound to all valid addresses.
PORT = 21567
BUFSIZ = 1024       # Size of the buffer
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)    # Create a socket.
tcpSerSock.settimeout(10)
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
        command = data

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
        return command, 0   # Returns 0 to set the timer of the motor state machine to zero seconds
    elif command == 'bearing': # Need to rework everything later...
        print('Received bearing cmd')
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
        self.state = 'stop'
        self.last_time = time()
        self.timer = 0.
        self.bearing = 0.
        # Sensory information:
        self.yaw = 0.

        self.pid = pid.PID()


    def set_state(self, new_state, arg=0.):
        if new_state == 'bearing':
            self.state = new_state
            self.bearing = float(arg)
        else:
            self.state = new_state
            self.timer = float(arg)

    def update(self, angle):
        self.yaw = angle

    def step(self):
        current_time = time()
        self.timer -= current_time - self.last_time
        self.last_time = current_time

        print(self.timer)

        if self.state == 'forward':
            if self.timer <= 0:
                motor.stop()
            else:
                motor.forward()
        elif self.state == 'backward':
            if self.timer <= 0:
                motor.stop()
            else:
                motor.backward()
        elif self.state == 'left':
            if self.timer <= 0:
                motor.stop()
            else:
                motor.left()
        elif self.state == 'right':
            if self.timer <= 0:
                motor.stop()
            else:
                motor.right()
        # Tentative:
        elif self.state == 'bearing':
            print(self.yaw, " vs. ", self.bearing)
            val = self.pid.compute(self.yaw-self.bearing)
            print("Value: {}".format(val))

            if val <= 0:
                motor.right(val)
            elif val >= 0:
                motor.left(val)

        elif self.state == 'stop':
            self.timer = 0.
            motor.stop()






# Needs a thorough rewrite
class MountStateMachine:
    def __init__(self):
        self.state = 'home_x_y'
        self.parameter = 0.

    def set_state(self, new_state):
        self.state = new_state

    def step(self):
        if self.state == ctrl_cmd[8]:
            pantilt.move_increase_x(self.parameter)
        elif self.state == ctrl_cmd[9]:
            pantilt.move_decrease_x(self.parameter)
        elif self.state == ctrl_cmd[10]:
            pantilt.move_increase_y(self.parameter)
        elif self.state == ctrl_cmd[11]:
            pantilt.move_decrease_y(self.parameter)
        elif self.state == ctrl_cmd[12]:
            pantilt.home_x_y()


class IMU(threading.Thread):
    def __init__(self, interface='/dev/ttyACM0'):
        super().__init__()
        self.imu_socket = serial.Serial(interface, 14400)
        self.last_reading = 0.0

    def run(self):
        while True:
            try:
                str = self.imu_socket.readline().decode()
                yaw = str.split('=')[1].split(',')[0]
                self.last_reading = float(yaw)
            except UnicodeDecodeError:
                pass

    def getYaw(self):
        return self.last_reading





if __name__=='__main__':
    # Initializing state machines:
    motor_sm = MotorStateMachine()
    mount_sm = MountStateMachine()

    #imu = IMU()
    #imu.start()

    while True:
        print('Waiting for connection...')
        # Waiting for connection. Once receiving a connection, the function accept() returns a separate
        # client socket for the subsequent communication. By default, the function accept() is a blocking
        # one, which means it is suspended before the connection comes.
        try:
            tcpCliSock, addr = tcpSerSock.accept()
            tcpCliSock.setblocking(0)   # Set socket to non-blocking; alternatively create new thread
        except:
            print("TCP-server timed out - no connection established.")
            sys.exit()

        print('...connected from :', addr)     # Print the IP address of the client connected with the server.

        # Main loop
        while True:
            try:
                data = tcpCliSock.recv(BUFSIZ).decode()
                # Analyze the command received and control the car accordingly.
                command, arg = getCommand(data)
                motor_sm.set_state(command, arg)
            except:
                #motor_sm.step()
                pass

            # Insert passive IMU-readout here:
            #print("Yaw=", imu.getYaw())
            #print("Is alive: ", imu.is_alive())

            #motor_sm.update(yaw)   # Update sensor input
            motor_sm.step()         # Execute step





tcpSerSock.close()
