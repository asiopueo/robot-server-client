#!/usr/bin/env python
#import RPi.GPIO as GPIO
#from RPiSim import GPIO
from fake_rpi.RPi import GPIO
import PCA9685 as p
import time    # Import necessary modules

# ===========================================================================
# Raspberry Pi pin11, 12, 13 and 15 to realize the clockwise/counterclockwise
# rotation and forward and backward movements
# ===========================================================================
Motor0 = 11  # pin11
Motor1 = 13  # pin13


# ===========================================================================
# Set channel 4 and 5 of the servo driver IC to generate PWM, thus
# controlling the speed of the car
# ===========================================================================
EN_M0    = 4  # servo driver IC CH4
EN_M1    = 5  # servo driver IC CH5

pins = [Motor0, Motor1]

# ===========================================================================
# Adjust the duty cycle of the square waves output from channel 4 and 5 of
# the servo driver IC, so as to control the speed of the car.
# ===========================================================================
def setSpeed(speed):
	speed *= 40
	print('speed is: ', speed)
	pwm.write(EN_M0, 0, speed)
	pwm.write(EN_M1, 0, speed)

def setup(busnum=None):
	global forward0, forward1, backward1, backward0
	global pwm
	if busnum == None:
		pwm = p.PWM()                  # Initialize the servo controller.
	else:
		pwm = p.PWM(bus_number=busnum) # Initialize the servo controller.

	pwm.frequency = 60
	forward0 = 'True'
	forward1 = 'True'
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)        # Number GPIOs by its physical location
	try:
		for line in open("config"):
			if line[0:8] == "forward0":
				forward0 = line[11:-1]
			if line[0:8] == "forward1":
				forward1 = line[11:-1]
	except:
		pass
	if forward0 == 'True':
		backward0 = 'False'
	elif forward0 == 'False':
		backward0 = 'True'
	if forward1 == 'True':
		backward1 = 'False'
	elif forward1 == 'False':
		backward1 = 'True'
	for pin in pins:
		GPIO.setup(pin, GPIO.OUT)   # Set all pins' mode as output

# ===========================================================================
# Control the DC motor to make it rotate clockwise, so the car will
# move forward.
# ===========================================================================

def motor0(x):
	if x == 'True':
		GPIO.output(Motor0, GPIO.LOW)
	elif x == 'False':
		GPIO.output(Motor0, GPIO.HIGH)
	else:
		print('Config Error')

def motor1(x):
	if x == 'True':
		GPIO.output(Motor1, GPIO.LOW)
	elif x == 'False':
		GPIO.output(Motor1, GPIO.HIGH)

def forward(speed = 25):
	setSpeed(speed)
	motor0(forward0)
	motor1(forward1)

def backward(speed = 25):
	setSpeed(speed)
	motor0(backward0)
	motor1(backward1)

def left(speed = 65):
	setSpeed(speed)
	motor0(backward0)
	motor1(forward1)

def right(speed = 65):
	setSpeed(speed)
	motor0(forward0)
	motor1(backward1)


def stop():
	setSpeed(0)
	for pin in pins:
		GPIO.output(pin, GPIO.LOW)

# ===========================================================================
# The first parameter(status) is to control the state of the car, to make it
# stop or run. The parameter(direction) is to control the car's direction
# (move forward or backward).
# ===========================================================================
def ctrl(status, direction=1):
	if status == 1:   # Run
		if direction == 1:     # Forward
			forward()
		elif direction == -1:  # Backward
			backward()
		else:
			print('Argument error! direction must be 1 or -1.')
	elif status == 0: # Stop
		stop()
	else:
		print('Argument error! status must be 0 or 1.')

def test():
	while True:
		setup()
		ctrl(1)
		time.sleep(3)
		setSpeed(10)
		time.sleep(3)
		setSpeed(100)
		time.sleep(3)
		ctrl(0)

if __name__ == '__main__':
	setup()
	setSpeed(25)
	#forward()
	#backward()
	stop()
