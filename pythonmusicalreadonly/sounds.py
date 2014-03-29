from musical.theory import Note, Scale, Chord
from musical.audio import playback

from timeline import Hit, Timeline

# Define key and scale
key = Note('D3')
scale = Scale(key, 'major')

# Grab progression chords from scale starting at the octave of our key
progression = Chord.progression(scale, base_octave=key.octave)
print progression

time = 0.0 # Keep track of currect note placement time in seconds

#####################

## Gesture: Arpeggio!
arpeggio_timeline = Timeline()

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

# Reduce volume to 25%
arpeggio_data = arpeggio_data * 0.25

#####################

## Gesture: Strum!
strum_timeline = Timeline()

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

# Reduce volume to 25%
strum_data = strum_data * 0.25

#####################

# Audio testing

print "Playing arpeggio audio..."
playback.play(arpeggio_data)

print "Playing strum audio..."
playback.play(strum_data)

print "Done!"
