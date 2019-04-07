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
#def forward_fun(event):
def forward_fun():
	print("forward")
	tcpCliSock.send('forward'.encode())

def backward_fun():
	print("backward")
	tcpCliSock.send(b'backward')

def left_fun():
	print('left')
	tcpCliSock.send(b'left')

def right_fun():
	print("right")
	tcpCliSock.send(b'right')



#####################
#	Camera commands
#####################
def x_increase(event):
	print("x+")
	tcpCliSock.send(b'x+')

def x_decrease(event):
	print("x-")
	tcpCliSock.send(b'x-')

def y_increase(event):
	print("y+")
	tcpCliSock.send(b'y+')

def y_decrease(event):
	print("y-")
	tcpCliSock.send(b'y-')

def xy_home(event):
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
