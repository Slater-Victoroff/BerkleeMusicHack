from musical.theory import Note, Scale, Chord
from musical.audio import playback

from timeline import Hit, Timeline

# Building upon example-01.py from the python-musical repo online
# For our Berklee Music Therapy hack project: arpeggio, strumming, single notes, drumbeat
# greenteawarrior

# Define key and scale
key = Note('D3')
scale = Scale(key, 'major')

# Grab progression chords from scale starting at the octave of our key
progression = Chord.progression(scale, base_octave=key.octave)
print progression


#####################
## Gesture: Arpeggio!
def arpeggio():

    arpeggio_timeline = Timeline()
    time = 0.0 # Keep track of currect note placement time in seconds

    # Add progression to timeline by arpeggiating chords from the progression
    for index in [0, 1]:
      chord = progression[index]
      root, third, fifth = chord.notes
      arpeggio = [root, third, fifth, third, root, third, fifth, third]
      for i, interval in enumerate(arpeggio):
        ts = float(i * 2) / len(arpeggio)
        arpeggio_timeline.add(time + ts, Hit(interval, 1.0))
      time += 2.0

    print "Rendering arpeggio audio..."
    arpeggio_data = arpeggio_timeline.render()

    return arpeggio_data


#####################
## Gesture: Strum!
def strum():
    strum_timeline = Timeline()
    time = 0.0 # Keep track of currect note placement time in seconds

    # Strum out root chord to finish
    chord = progression[0]
    strum_timeline.add(time + 0.0, Hit(chord.notes[0], 4.0))
    strum_timeline.add(time + 0.1, Hit(chord.notes[1], 4.0))
    strum_timeline.add(time + 0.2, Hit(chord.notes[2], 4.0))
    strum_timeline.add(time + 0.3, Hit(chord.notes[1].transpose(12), 4.0))
    strum_timeline.add(time + 0.4, Hit(chord.notes[2].transpose(12), 4.0))
    strum_timeline.add(time + 0.5, Hit(chord.notes[0].transpose(12), 4.0))

    print "Rendering strum audio..."
    strum_data = strum_timeline.render()

    return strum_data

#####################
## Playing a data file at a particular volume

def play(data, volume=0.25) :
    # input is a proportion. 0<volume<1
    # example: a volume input of 0.25 makes it play at 25% volume

    # Reduce volume to the specified number 
    data = data * volume

    print "Playing the audio file..."
    playback.play(data)

    return

# Audio testing
print "Playing arpeggio audio..."
play(arpeggio(), 0.25)

print "Playing strum audio..."
play(strum(), 0.5)

print "Done!"
