import operator

from musical.theory import Note, Scale, Chord
from musical.audio import playback

from timeline import Hit, Timeline

# Building upon example-01.py from the python-musical repo online
# For our Berklee Music Therapy hack project: arpeggio, strumming, single notes
# greenteawarrior

# Define key and scale
key = Note('D#3')
scale = Scale(key, 'major')

# Grab progression chords from scale starting at the octave of our key
progression = Chord.progression(scale, base_octave=key.octave)
# print progression

def chord_progression(func):
    def generate_progression(*args, **kwargs):
        if not kwargs.get('progression', False):
            kwargs['key'] = Note(kwargs.get('note', 'D3'))
            kwargs['scale'] = Scale(kwargs['key'], kwargs.get('scale', 'major'))
            kwargs['progression'] = Chord.progression(kwargs['scale'], base_octave=kwargs['key'].octave)
        return func(*args, **kwargs)
    return generate_progression

#####################
## Gesture: Arpeggio!
@chord_progression
def arpeggio(*args, **kwargs):

    arpeggio_timeline = Timeline()
    time = 0.0 # Keep track of currect note placement time in seconds

    # Add progression to timeline by arpeggiating chords from the progression
    for index in [0, 1]:
      chord = kwargs['progression'][index]
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
@chord_progression
def strum(*args, **kwargs):
    strum_timeline = Timeline()
    time = 0.0 # Keep track of currect note placement time in seconds

    # Strum out root chord to finish
    chord = kwargs['progression'][0]
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
## Gesture: Single note!
@chord_progression
def singlenote(note_number, *args, **kwargs):
    singlenote_timeline = Timeline()
    time = 0.0 # Keep track of currect note placement time in seconds

    # Strum out root chord to finish
    chord = kwargs['progression'][0]
    singlenote_timeline.add(time + 0.0, Hit(chord.notes[note_number], 3.0))

    print "Rendering singlenote audio..."
    singlenote_data = singlenote_timeline.render()

    return singlenote_data

#####################
## Chord things!
@chord_progression
def multinote(note_dict, *args, **kwargs):
    """
    note_dict should be of the form:
    [
    [note_number1, volume1],
    [note_numer2, volume2],
    ...
    ]
    """
    notes = [singlenote(number[0], *args, **kwargs) for number in note_dict]
    # print notes
    notes_vols = [number[1] for number in note_dict]
    # print notes_vols
    return reduce(operator.add, [note * volume for note, volume in zip(notes, notes_vols)])

#####################
## Multilayered things!
@chord_progression
def multilayer(layers_input, *args, **kwargs):
    """
    layers_input should be of the form:
    [
    ["arpeggio", volumeint],
    ["strum", volumeint],
    ["singlenote", volumeint, notenumberint],
    ["multinote", volumeint, note_dict]
    ]
    """

    layerslength = len(layers_input) 
    layers = [0] * (layerslength)
    layersvols = [0] * (layerslength)

    for i in range(len(layers_input)):
        currentlayer = layers_input[i]
        layertype = currentlayer[0]
        layervolume = currentlayer[1]
        layersvols[i] = layervolume

        if layertype == "arpeggio":
            layers[i] = arpeggio(*args, **kwargs)
        elif layertype == "strum":
            layers[i] = strum(*args, **kwargs)
        elif layertype == "singlenote":
            note_number = currentlayer[2]
            layers[i] = singlenote(note_number, *args, **kwargs)
        elif layertype == "multinote":
            note_dict = currentlayer[2]
            layers[i] = multinote(note_dict, *args, **kwargs)

    returnme =  reduce(operator.add, [note * volume for note, volume in zip(layers, layersvols)])
    print returnme
    return returnme

#####################
## Playing a data file at a particular volume
def play(data, volume=1) :
    # input is a proportion. 0<volume<1
    # example: a volume input of 0.25 makes it play at 25% volume

    # Reduce volume to the specified number 
    data = data * volume

    # Playing the audio
    print "Playing the audio file..."
    playback.play(data)

    return

#####################
# Audio testing
# print "Playing arpeggio audio..."
# play(arpeggio(), 0.25)

# # Trying to do continuous arpeggio?

# print "Playing strum audio..."
# # play(strum(), 0.5)

# print "Playing single note audio..."
# first = singlenote(0)
# play(first, 0.5)
# play(first, 0.5)
# play(first, 0.5)

# print "Playing strum audio..."
# play(strum(), 0.5)

# print "Playing single note audio..."
# first = singlenote(0)
# play(multinote({0:10, 1: 10, 2:10}, note="A3", scale="pentatonicmajor"))

# play(multinote([[0,0], [1,5], [2,5]], note="A3", scale="pentatonicmajor"))

# multilayer([{"layertype": "singlenote", "volume": .5, "note_number": 1}], note="A3", scale="pentatonicmajor")

multilayer([["arpeggio", 2], ["arpeggio", 3]], note="A3", scale="pentatonicmajor")


print "Done!"
