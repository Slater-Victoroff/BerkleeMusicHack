import math
import time

def extract_mag_and_phase(vector):
    """
    Return the phase and magnitude of the 
    frame vector [dx,dy]
    """
    vector = list(vector)
    scaling_factor = math.sqrt(vector[0]**2 + vector[1]**2)
    vector[0] = vector[0] * (1./scaling_factor)
    vector[1] = vector[1] * (1./scaling_factor)
    phase = degrees(math.atan(vector[1]/vector[0]) % math.pi)
    mag = math.sqrt(vector[0]**2+vector[1]**2)
    return [mag, phase]

def get_note(phase):
    """
    Figure out what range the phase is in
    """
    phase = degrees(phase)
    print phase
    note_phases = {'G':[18,90],'C':[90,162],'E':[162,234],'A':[234,306],'D':[306,18]}
    for note, p_range in note_phases.iteritems():
        if phase%360 < p_range[1] and phase%360 >= p_range[0]:
            return note

def degrees(phase):
    if phase<0:
        phase = 2*math.pi+phase
    return phase/math.pi*180

def get_volume(mag,threshold,c):
    """
    Some constant times the magnitude = volume 
    unless magnitude is below a threshold
    """
    if mag > threshold:
        return c*mag
    else:
        return 0

def note_delay(prev_time, prev_note, cur_note, tmax=1):
    """
    If the note for this frame is the same as the last, 
    don't do anything until tmax seconds have passed
    or another note is played
    """
    while prev_note == cur_note:
        time_delta = time.time() - prev_time ## old time being the last time that note was played
        if time_delta >= tmax: #seconds
            ## play the note again
            prev_time = time.time()
            prev_note = cur_note
        else:
            ## be silent
            pass
