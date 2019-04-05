#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import client_backend

################################################
#
#	PyQt4
#
################################################

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MainWindow(QDialog):
	def __init__(self):
		super(MainWindow, self).__init__()
		# Define buttons
		forwardButton = QPushButton("Forward")
		leftButton = QPushButton("Left")
		neutralButton = QPushButton("Neutral")
		rightButton = QPushButton("Right")
		backwardButton = QPushButton("Backward")
		quitButton = QPushButton("Quit")

		gridLayout = QGridLayout()
		gridLayout.addWidget(forwardButton, 0, 1)
		gridLayout.addWidget(leftButton, 1, 0)
		gridLayout.addWidget(neutralButton, 1, 1)
		gridLayout.addWidget(rightButton, 1, 2)
		gridLayout.addWidget(backwardButton, 2, 1)

		windowLayout = QVBoxLayout()
		windowLayout.addLayout(gridLayout)
		windowLayout.addWidget(quitButton)
		self.setLayout(windowLayout)
		self.show()


		forwardButton.clicked.connect(client_backend.forward_fun)
		leftButton.clicked.connect(client_backend.left_fun)
		neutralButton.clicked.connect(client_backend.neutral_fun)
		rightButton.clicked.connect(client_backend.right_fun)
		backwardButton.clicked.connect(client_backend.backward_fun)
		quitButton.clicked.connect(client_backend.quit_fun)


"""
label = Label(top, text='Speed:', fg='red')  # Create a label
label.grid(row=6, column=0)                  # Label layout

speed = Scale(top, from_=0, to=100, orient=HORIZONTAL, command=changeSpeed)  # Create a scale
speed.set(50)
speed.grid(row=6, column=1)
"""
def main():
	app = QApplication(sys.argv)
	ex = MainWindow()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
