"""Not functional right now, just a thing to stick in other code later"""

import cv2
import time
import numpy as np

import cv2

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
		print np.mean(self.pixels), np.mean(blank())
		self.pixels = blank() - (blank() - self.pixels)/2

class Circle(object):

	def __init__(self, canvas, center, radius, color):
		self.x = center[0]
		self.y = center[1]
		self.r = radius
		self.color = color
		self.canvas = canvas
		self.display()

	def update(self, dx=0, dy=0, dr=0, color=None):
		self.display()
		self.x += dx
		self.y += dy
		self.r += dr
		self.r = max(1, self.r)
		if color:
			self.color = color
		self.display()

	def display(self):
		cv2.circle(self.canvas.pixels, (self.x, self.y), self.r, self.color, -1)
 
canvas = Canvas(frame.shape[1], frame.shape[0])
color = np.array([120, 0, 0])
c = Circle(canvas=canvas, center=(canvas.x/2, canvas.y/2), radius=20, color=color)

while rval:
	rval, frame = vc.read()
	key = cv2.waitKey(20)
	if key == 27: # exit on ESC
		break

	# drawing	
	canvas.fade()
	c.update(dx=np.random.randint(-5, 6), dy=np.random.randint(-5, 6), dr=np.random.randint(-1, 2))
	cv2.imshow("preview", canvas.pixels)
    ## (50,50) will be changed to the value of the key point position

cv2.destroyWindow("preview")




