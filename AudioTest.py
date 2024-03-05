import pyaudio
import wave
import librosa
import math
import matplotlib.pyplot as plt
from scipy.datasets import electrocardiogram
from scipy.signal import find_peaks
import numpy as np
from collections import Counter
from music21 import note
import scipy.signal

from switchblade.audio_datasets.get_dataset import get_dataset

# Define high-pass filter
def high_pass_filter(data, cutoff_freq, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff_freq / nyq
    b, a = scipy.signal.butter(order, normal_cutoff, btype='high', analog=False)
    filtered_data = scipy.signal.lfilter(b, a, data)
    return filtered_data

# def butter_lowpass_filter(data, cutoff, fs, order=5):
#     nyq = 0.5 * fs
#     normal_cutoff = cutoff / nyq
#     b, a = scipy.signal.butter(order, normal_cutoff, btype='low', analog=False)
#     y = scipy.signal.lfilter(b, a, data)
#     return y

# Function to calculate RMS amplitude
def calculate_rms(data):
    """Calculate the root mean square amplitude of the given audio block."""
    count = len(data)/2
    format = np.int16
    audio_data = np.frombuffer(data, dtype=format)
    rms = np.sqrt(np.mean(np.square(audio_data), axis=0))
    return rms

def amplitude_filter(data, threshold):
    """Zeroes out data below the specified amplitude threshold."""
    return np.where(abs(data) > threshold, data, 0.0)

class AudioHandler(object):
    def __init__(self):
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 2048
        self.p = None
        self.stream = None

        # High-pass filter parameters
        self.cutoff_frequency = 70.0

        # Amplitude Threshold
        self.amplitude_threshold = 20.0

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
    seconds = 10
    for i in range(0, int(audio.RATE / audio.CHUNK * seconds)):
        # data = stream.read(CHUNK)
        # frames.append(data)

        # Reads the data
        data = audio.stream.read(audio.CHUNK)
        array_data = np.frombuffer(data, dtype=np.float32)
        amplitude = calculate_rms(data)
        midi = 0
        if(np.abs(amplitude) > audio.amplitude_threshold):
            #amplitude_data = amplitude_filter(array_data, audio.amplitude_threshold)
            filtered_data = high_pass_filter(array_data, audio.cutoff_frequency, audio.RATE)
            filtered_data = butter_lowpass_filter(filtered_data, 120, audio.RATE)
            midi = midi_number_detection(filtered_data, audio.RATE)
            print("Amplitude = ", calculate_rms(data))

        if(midi != 0):
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
    

if __name__ == '__main__':
    main()

