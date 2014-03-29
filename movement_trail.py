"""Not functional right now, just a thing to stick in other code later"""

import cv2
import time


import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

def fading_circle(circ_args):
	## time.sleep will be changed to 1/frame rate
	time.sleep(0.05)
	radius = circ_args[2]
	cv2.circle(*circ_args)
	if radius > 0:
		circ_args[2] -= 1
		return fading_circle(circ_args)
	## I know it doesn't look like anything right now
	print radius

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    ## (50,50) will be changed to the value of the key point position
    circ_args = [frame,(50,50),5,(3,65,26,.5),-1]
	fading_circle(circ_args)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")




