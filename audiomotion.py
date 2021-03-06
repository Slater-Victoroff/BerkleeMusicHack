import cv2
import numpy as np
import map_cvdata as mc
import sounds
import signal
import server
import sys
from timeline import Beat
import multiprocessing

def signalHandler(signal,frame):
    print('exiting')
    p1.terminate()
    raise SystemExit
    sys.exit()

xx,yy = np.meshgrid(np.arange(640),np.arange(480))
dxs = []
dys = []
xs = [640/2]
ys = [480/2]
cam = cv2.VideoCapture(0)
ret,frame = cam.read()
greyscale = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
greyscale = cv2.GaussianBlur(greyscale,(5,5),0)
vis = disp = np.float32(greyscale) 
dataQueue=multiprocessing.Queue()
p1=multiprocessing.Process(target=server.main,args=(dataQueue,))
p1.start()
signal.signal(signal.SIGINT,signalHandler)
while True:
    ret,frame = cam.read()

    greyscale = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    greyscale = cv2.GaussianBlur(greyscale,(5,5),0)
    cv2.accumulateWeighted(greyscale,vis,.9,None)
    runavg = cv2.convertScaleAbs(vis)
    disp=greyscale-vis
#    cv2.imshow('movement',disp)
#    pyplot.show()
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

    vecs = (dxs[-1],dys[-1]) 
    magPhase = mc.extract_mag_and_phase(vecs)
    note = mc.get_note(magPhase[1])
    measurement = {'x':xs[-1],'y':ys[-1],'note':note}
    if (xs[-1] != np.nan) and (ys[-1] != np.nan):
        dataQueue.put(measurement)
    #volume = mc.get_volume(magPhase[0],0,1)
    #sounds.play(sounds.arpeggio(note=note,scale='pentatonicmajor'))
    #beat = Beat('drumbeat2.wav',10,6)
    #volume = mc.get_volume(magPhase[0],0,1)
    #sounds.play(sounds.singlebeat(beat))
