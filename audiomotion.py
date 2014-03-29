import cv2
import numpy as np
import map_cvdata as mc
import sounds
import server
import sys

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
p1=multiprocessing.Process(target=server.main,args=(dataQueue))
p1.start()
signal.signal(signal.SIGINT,signalHandler)
while True:
    ret,frame = cam.read()

    greyscale = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    greyscale = cv2.GaussianBlur(greyscale,(5,5),0)
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

    vecs = (dxs[-1],dys[-1]) 
    magPhase = mc.extract_mag_and_phase(vecs)
    print magPhase
    note = mc.get_note(magPhase[1])
    measurement = {'x':xs[-1],'y':ys[-1],'r':magPhase[0],'note':note}
    dataQueue.put(measurement)
    #print note
    #volume = mc.get_volume(magPhase[0],0,1)
    #sounds.play(sounds.arpeggio(note=note,scale='pentatonicmajor'))
def signalHandler(signal,frame):
    print('exiting')
    p1.terminate()
    raise SystemExit
    sys.exit()
