import operator

from musical.theory import Note, Scale, Chord
from musical.audio import playback

from timeline import Hit, Timeline

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
## Gesture: Strum!
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

@chord_progression
def multinote(note_dict, *args, **kwargs):
    """
<<<<<<< HEAD
note_dict should be of the form:
{
note_number1: volume1,
note_numer2: volume2,
...
}
"""
    notes = [singlenote(number, *args, **kwargs) for number in note_dict]
    return reduce(operator.add, [note * volume for note, volume in zip(notes, note_dict)])
=======
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

<<<<<<< HEAD
    for i in range(len(layers_input)):
=======
    biggest = 0

    for i in range(len(layers_input)):
        #check for biggest-ness here.

>>>>>>> 61600df358e00d17c9fd8aaaec50d60085c441b6
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

<<<<<<< HEAD
    returnme =  reduce(operator.add, [note * volume for note, volume in zip(layers, layersvols)])
    print returnme
    return returnme
    #     for l in layers_input:
    #         layertype = l["layertype"]
    #         layervolume = l["volume"]
    #         layersvols[i] = layervolume

    #         if layertype == "arpeggio":
    #             layers[i] = arpeggio(*args, **kwargs)
    #         elif layertype == "strum":
    #             layers[i] = strum(*args, **kwargs)
    #         elif layertype == "singlenote":
    #             note_number = l["note_number"]
    #             layers[i] = singlenote(note_number, *args, **kwargs)
    #         elif layertype == "multinote":
    #             note_dict = l["note_dict"]
    #             layers[i] = multinote(note_dict, *args, **kwargs)

    # print layers
    # print layers_input
    # return


@chord_progression
def notes_and_beat(notes, beat, *args, **kwargs):
    """
    notes should be the result of multinote or singlenote
    beat should be results of singlebeat
    """
=======
    biggest = layers[0].shape
    print biggest

    returnme =  reduce(add, [note * volume for note, volume in zip(layers, layersvols)])
    print zip(layers, layersvols)
    print returnme.shape
    return returnme


def add(a, b):
    # pairs = (a.shape[0], a), (b.shape[0], b)
    # smaller, larger = min(pairs(,. max(pairs)
    d = {a.shape[0]: a, b.shape[0]: b}
    smaller, larger = d[min(d.keys())], d[max(d.keys())]
    larger[:smaller.shape[0]] += smaller
    return larger


#####################
## Doing some beats shenanigans
@chord_progression
def notes_and_beat(notes, beat, *args, **kwargs):
    """
    notes should be the result of multinote or singlenote
    beat should be results of singlebeat
    """
>>>>>>> 61600df358e00d17c9fd8aaaec50d60085c441b6
    if len(beat) > len(notes):
        res = beat.copy()
        res[:len(notes)] += notes
    else:
        res = notes.copy()
        res[:len(beat)] += beat
    return res
>>>>>>> 7e54cd4d3d4a18007c1b0913d8673bfa44266ed0

#####################
## Playing a data file at a particular volume
def play(data, volume=0.25) :
    # input is a proportion. 0<volume<1
    # example: a volume input of 0.25 makes it play at 25% volume

    # Reduce volume to the specified number
    data = data * volume

    # Playing the audio
    print "Playing the audio file..."
    playback.play(data)

<<<<<<< HEAD
    return
=======
    return


#####################
# Audio testing

<<<<<<< HEAD
# # Trying to do continuous arpeggio?

# print "Playing strum audio..."
# # play(strum(), 0.5)

=======
>>>>>>> 61600df358e00d17c9fd8aaaec50d60085c441b6
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

<<<<<<< HEAD
# multilayer([["arpeggio", 2], ["arpeggio", 3]], note="A3", scale="pentatonicmajor")
# play(notes_and_beat(multinote({0:10, 1: 10, 2:10}), singlebeat(Beat('drumbeat2.wav')), note="A3", scale="pentatonicmajor"))

=======
multilayer([["arpeggio", 2], ["arpeggio", 3]], note="A3", scale="pentatonicmajor")
>>>>>>> 61600df358e00d17c9fd8aaaec50d60085c441b6

>>>>>>> 7e54cd4d3d4a18007c1b0913d8673bfa44266ed0
