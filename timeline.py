from collections import defaultdict

from musical.audio import source

from scipy.io.wavfile import read

import numpy as np

# XXX: Early implementation of timeline/hit concepts. Needs lots of work

# TODO: Associate sound source with Hit instances somehow
# TODO: Amplitude, possibly other dynamics attributes


class Hit:

  ''' Rough draft of Hit class. Stores information about the hit and generates
      the audio array accordingly. Currently implements a basic cache to avoid
      having to rerender identical hits
  '''

  cache = {}

  def __init__(self, note, length):
    self.note = note
    self.length = length

  def render(self):
    # Render hit of "key" for "length" amount of seconds
    # XXX: Currently only uses a string pluck
    key = (str(self.note), self.length)
    if key not in Hit.cache:
      Hit.cache[key] = source.pluck(self.note, self.length)
    return Hit.cache[key]

class Beat:
  ''' Adding a beat class for looping audio files
  '''

  def __init__(self, filename, loops, length):
    self.filename = filename
    self.loops = loops
    self.length = length*loops

  def render(self):
    ''' Returns the wav file converted to a numpy array
    '''
    sound = read(self.filename)
    data = np.array(sound[1],dtype=float)
    # average between channels
    data = (data[:,0]+data[:,1])/2

    def rescale(val, in_min, in_max, out_min, out_max):
      return out_min + (val - in_min) * ((out_max - out_min) / (in_max - in_min))

    # rescale to between 0 and 1 so it doesn't blow the speakers
    data = rescale(data, data.min(), data.max(), -1, 1)

    i = self.loops - 1
    newdata = data
    while i>0:
      newdata = np.concatenate((newdata,data))
      i-=1

    return newdata


class Timeline:

  ''' Rough draft of Timeline class. Handles the timing and mixing of Hits
  '''

  def __init__(self, rate=44100):
    self.rate = rate
    self.hits = defaultdict(list)

  def add(self, time, hit):
    # Add "hit" at "time" seconds in
    self.hits[time].append(hit)

  def calculate_length(self):
    # Determine length of playback from end of last hit
    length = 0.0
    for time, hits in self.hits.items():
      for hit in hits:
        length = max(length, time + hit.length)
    return length

  def render(self):
    # Return timeline as audio array by rendering the hits
    out = source.silence(self.calculate_length())
    for time, hits in self.hits.items():
      index = int(time * self.rate)
      for hit in hits:
        data = hit.render()
        out[index:index + len(data)] += data
    return out

