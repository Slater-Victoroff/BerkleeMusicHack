import cv2
import numpy as np
from matplotlib import pyplot as plt
from time import time,sleep
from sklearn.cluster import KMeans

xx,yy = np.meshgrid(np.arange(640),np.arange(480))
dxs = []
dys = []
xs = [640/2]
ys = [480/2]

def getVectors(frame,vis):
    greyscale = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    greyscale = cv2.GaussianBlur(greyscale,(5,5),0)
    disp = np.float32(greyscale) 
    if vis==None:vis=np.copy(disp)
    cv2.accumulateWeighted(greyscale,vis,.9,None)
    runavg = cv2.convertScaleAbs(vis)
    disp=greyscale-vis
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
    return (dxs[-1],dys[-1])
