#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import socket

ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']


#HOST = '192.168.0.147'    # Server(Raspberry Pi) IP address
HOST = 'localhost'

PORT = 21567
BUFSIZ = 1024             # buffer size
ADDR = (HOST, PORT)

tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Create a socket
try:
	tcpCliSock.connect(ADDR)
except:
	pass

######################
#	Vehicle commands
######################
DEFAULT_TIME=3 # 3000 seconds
DEFAULT_ANGLE=20 # 20 degrees

#def forward_fun(event):
def forward_fun(arg=DEFAULT_TIME):
	data = "forward={}".format(arg)
	print(data)
	tcpCliSock.send(data.encode())

def backward_fun(arg=DEFAULT_TIME):
	data = "backward={}".format(arg)
	print(data)
	tcpCliSock.send(data.encode())

def left_fun(arg=DEFAULT_TIME):
	data = "left={}".format(arg)
	print(data)
	tcpCliSock.send(data.encode())

def right_fun(arg=DEFAULT_TIME):
	data = "right={}".format(arg)
	print(data)
	tcpCliSock.send(data.encode())

def stop_fun():
	print('stop')
	tcpCliSock.send(b'stop')


#####################
#	Camera commands
#####################
def x_increase(arg=DEFAULT_ANGLE):
	data = "x+={}".format(arg)
	print(data)
	tcpCliSock.send(data.encode())

def x_decrease(arg=DEFAULT_ANGLE):
	data = "x-={}".format(arg)
	print(data)
	tcpCliSock.send(data.encode())

def y_increase(arg=DEFAULT_ANGLE):
	data = "y+={}".format(arg)
	print(data)
	tcpCliSock.send(data.encode())

def y_decrease(arg=DEFAULT_ANGLE):
	data = "y-={}".format(arg)
	print(data)
	tcpCliSock.send(data.encode())

def xy_home():
	print("xy_home")
	tcpCliSock.send(b'xy_home')

# =============================================================================
# Exit the GUI program and close the network connection between the client
# and server.
# =============================================================================
def quit_fun():
	tcpCliSock.send(b'stop')
	tcpCliSock.close()
	sys.exit()


"""
spd = 50

def changeSpeed(ev=None):
	tmp = 'speed'
	global spd
	spd = speed.get()
	data = tmp + str(spd)  # Change the integers into strings and combine them with the string 'speed'.
	print("sendData = %s" % data)
	tcpCliSock.send(data)  # Send the speed data to the server(Raspberry Pi)



speed = Scale(top, from_=0, to=100, orient=HORIZONTAL, command=changeSpeed)  # Create a scale
speed.set(50)
speed.grid(row=6, column=1)
"""
