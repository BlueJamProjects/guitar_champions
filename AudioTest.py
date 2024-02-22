import pyaudio
import wave
import librosa
import time
import struct
import math
import matplotlib.pyplot as plt
from scipy.datasets import electrocardiogram
from scipy.signal import find_peaks
import numpy as np
from collections import Counter
from music21 import note
import switchblade
import nnAudio

from switchblade.audio_datasets.get_dataset import get_dataset

power = 12

class AudioHandler(object):
    def __init__(self):
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.p = None
        self.stream = None

    def start(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  output=False,
                                  frames_per_buffer=self.CHUNK)

    def stop(self):
        self.stream.close()
        self.p.terminate()

    


### Midi number detection ###
def midi_number_detection(audio, sr):

  midi_numbers_list = []

  # Compute cqt
  cqt = np.abs(librosa.cqt(audio, sr=sr))

  # Detect the peak of each time frame
  #   - cqt.shape[0]: number of frequency bins
  #   - cqt.shape[1]: number of time frames

  for i in range(cqt.shape[1]):
      frame = cqt[:, i]

      # array of indices corresponding to the peaks
      # we can fine-tune the parameter of find_peaks in the future testing
      peaks = find_peaks(frame, height=0.000001)[0]

      if peaks.size > 0:
          dominant_peak = peaks[np.argmax(frame[peaks])]

          # convert to frequecy
          frequency = librosa.cqt_frequencies(n_bins=cqt.shape[0], fmin=32.7)[dominant_peak]

          # Convert frequency to midi_number
          midi_number = librosa.hz_to_midi(frequency)
          midi_numbers_list.append(midi_number)

  midi_counts = Counter(midi_numbers_list)
  return midi_counts



def main():

    audio = AudioHandler()

    audio.start()
    print("start recording... ")
    total = 0
    count = 0
    seconds = 3
    for i in range(0, int(audio.RATE / audio.CHUNK * seconds)):
        # data = stream.read(CHUNK)
        # frames.append(data)

        # Reads the data
        data = np.frombuffer(audio.stream.read(audio.CHUNK), dtype=np.float32)
        midi = midi_number_detection(data, audio.RATE)

        if len(midi) == 0:
            continue
        m = round(midi.most_common(1)[0][0])
        midi_num_test = 50

        count = 0

        if(m == midi_num_test):
            count += 1
        total += 1

        print('Midi Number Prediction = ', m)
    
    print("recording stopped")
    audio.stop()

    print('Accuracy = ', count/total*100)
    

if __name__ == '__main__':
    main()

