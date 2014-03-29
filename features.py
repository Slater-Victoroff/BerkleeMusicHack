import cv2
import numpy as np

mser=cv2.MSER()
#mser does significantly better on color than greyscale
fast=cv2.FastFeatureDetector()
surf=cv2.SURF()
orb=cv2.ORB()
sift=cv2.SIFT()
brisk=cv2.BRISK()

cam = cv2.VideoCapture(0)
ret,frame = cam.read()
#f1=cv2.medianBlur(frame,7)
#f2=cv2.medianBlur(f1,7)
dddd = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
vis = disp = np.float32(dddd) 
while True:
    ret,frame = cam.read()
    dddd = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #f1=cv2.medianBlur(frame,7)
    #f2=framecv2.medianBlur(f1,7)
    flag,f2 = cv2.threshold(dddd,100,120,cv2.THRESH_BINARY)
    #kp=mser.detect(f2,None)
    #hulls =[cv2.convexHull(p.reshape(-1,1,2)) for p in kp]

    #cv2.polylines(vis,hulls,1,(0,0,255))
    #kp=sift.detect(f2,None)
    #vis=cv2.drawKeypoints(f2,kp)
    cv2.accumulateWeighted(f2,vis,.9,None)
    runavg = cv2.convertScaleAbs(vis)
    disp=f2-vis
    cv2.imshow('features',disp)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cam.release()
        cv2.destroyAllWindows()
        break
