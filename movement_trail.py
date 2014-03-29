"""Not functional right now, just a thing to stick in other code later"""

import cv2
import time
import numpy as np
import pygame
import random

screen = pygame.display.set_mode((0,0)) 
screen = dict(zip(("x", "y"), screen.get_size())) 

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

blank = lambda: np.ones(frame.shape, np.uint8)*255;

class Canvas(object):

	def __init__(self, x, y, pixels=blank()):
		self.x = x
		self.y = y
		self.pixels = pixels

	def clean(self):
		self.pixels = blank()

	def fade(self):
		self.pixels = blank() - (blank() - self.pixels)/2

	def update(self):
		self.pixels = cv2.blur(canvas.pixels, (3,3))
		cv2.imshow("preview", cv2.resize(self.pixels, (0,0), fx=2, fy=2))

class Circle(object):

	def __init__(self, canvas, center, radius, color):
		self.x = center[0]
		self.y = center[1]
		self.r = radius
		self.color = color
		self.canvas = canvas
		self.display()

	def update(self, x=0, y=0, r=0, color=None):
		self.display()
		self.x = x
		self.y = y
		self.r = max(1, r)
		if color != None:
			self.color = np.array(color)
		self.display()

	def display(self):
		cv2.circle(self.canvas.pixels, (self.x, self.y), self.r, self.color, 5)
 
colors = [np.array([156, 188, 26]),
		  np.array([113, 204, 46]), 
		  np.array([219, 152, 52]), 
		  np.array([15, 196, 241]), 
		  np.array([182, 89, 155])]

canvas = Canvas(frame.shape[1], frame.shape[0])
c = Circle(canvas=canvas, center=(canvas.x/2, canvas.y/2), radius=20, color=colors[0])

while rval:
	rval, frame = vc.read()
	key = cv2.waitKey(20)
	if key == 27: # exit on ESC
		break

	# drawing	
	color = None if random.random() < 0.9 else random.choice(colors)
	c.update(x= c.x + np.random.randint(-5, 6), y= c.y + np.random.randint(-5, 6), r= c.r + np.random.randint(-1, 2), color=color)
	canvas.update()
	canvas.fade()

cv2.destroyWindow("preview")




