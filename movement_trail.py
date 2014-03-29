"""Not functional right now, just a thing to stick in other code later"""

import cv2
import time

def fading_circle(circ_args):
	## time.sleep will be changed to 1/frame rate
	time.sleep(0.05)
	radius = circ_args[2]
	cv2.circle(*circ_args)
	if radius > 0:
		print radius
		circ_args[2] -= 1
		return fading_circle(circ_args)
	else:
		## take this out later
		print radius

## (50,50) will be changed to the value of the key point position
circ_args = [frame,(50,50),5,(3,65,26,.5),-1]
fading_circle(circ_args)