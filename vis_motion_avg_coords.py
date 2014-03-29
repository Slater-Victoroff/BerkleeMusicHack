import cv2
import numpy as np
from matplotlib import pyplot as plt
from time import time,sleep
from sklearn.cluster import KMeans

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
    dddd = cv2.GaussianBlur(dddd,(5,5),0)
    cv2.accumulateWeighted(dddd,vis,.9,None)
    runavg = cv2.convertScaleAbs(vis)
    disp=dddd-vis
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
    plt.scatter(np.mean(xs[-3:]),np.mean(ys[-3:]))
    plt.xlim([0,640])
    plt.ylim([0,480])
    fig.canvas.draw()
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cam.release()
        cv2.destroyAllWindows()
        break
