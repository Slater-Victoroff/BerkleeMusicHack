import cv2
import numpy as np
from matplotlib import pyplot as plt
from time import time,sleep

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
xx,yy = np.meshgrid(np.arange(640),np.arange(480))
fig = plt.figure()
dxs = []
dys = []
xs = [640/2]
ys = [480/2]
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
    # disp=cv2.medianBlur(disp,5)
    pmask = np.abs(disp) > 5
    x = np.mean(640-xx[pmask])
    y = np.mean(480-yy[pmask])
    dxs.append(xs[-1]-x)
    dys.append(ys[-1]-x)

    if np.sum(pmask) > 2000:
        xs.append(x)
        ys.append(y)
    else:
        xs.append(xs[-1])
        ys.append(ys[-1])

    cv2.imshow('features',disp)
    plt.clf()
    plt.plot(xs,ys)
    plt.xlim([0,640])
    plt.ylim([0,480])
    fig.canvas.draw()
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cam.release()
        cv2.destroyAllWindows()
        break
