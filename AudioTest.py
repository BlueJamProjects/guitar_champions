import pyaudio
import wave
import librosa
import math
from scipy.signal import find_peaks
import numpy as np
from collections import Counter
import scipy.signal
import crepe
from music21 import note

# Define bandpass filter
def butter_bandpass_filter(data, lowcut, highcut, sr, order=5):
    """
    Apply a bandpass filter to the audio data.
    """
    nyquist = 0.5 * sr
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = scipy.signal.butter(order, [low, high], btype='band')
    y = scipy.signal.lfilter(b, a, data)
    return y


def test():
    print("Hello")

def get_energy_around_freq(signal, sr, freq, bandwidth=5):
    """
    Calculate the energy of the signal around a specific frequency using FFT.


    Parameters:
    - signal: The audio signal (numpy array).
    - sr: The sampling rate of the audio signal.
    - freq: The target frequency around which to calculate energy.
    - bandwidth: The bandwidth around the target frequency (in Hz).


    Returns:
    - The energy of the signal within the specified bandwidth around the target frequency.
    """
    # Perform FFT
    fft_result = np.fft.fft(signal)
    # Get frequencies for FFT results
    freqs = np.fft.fftfreq(len(signal), 1/sr)
   
    # Find index range for target frequency +/- bandwidth
    lower_bound = freq - bandwidth / 2
    upper_bound = freq + bandwidth / 2
    target_indices = np.where((freqs >= lower_bound) & (freqs <= upper_bound))
   
    # Calculate energy in the target frequency band
    energy = np.sum(np.abs(fft_result[target_indices])**2)
   
    return energy




def midi_number_to_pitch(midi_number):
    n = note.Note()
    n.pitch.midi = midi_number
    return n.pitch.nameWithOctave

def audio_callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.float32)


    # Apply bandpass filter
    filtered_audio = butter_bandpass_filter(audio_data, lowcut=80, highcut=7000, sr=44100)


    try:
        time, frequency, confidence = crepe.predict(filtered_audio, 44100, viterbi=True)
       
        if len(confidence) > 0:
            best_idx = np.argmax(confidence)
            freq = frequency[best_idx]
            midi_number = librosa.hz_to_midi(freq)

            amplitude = np.sqrt(np.mean(filtered_audio**2))
            print(f"Pitch: {midi_number_to_pitch(midi_number)}, Frequency: {freq:.2f} Hz, Confidence: {confidence[best_idx]:.2f}, Amplitude: {amplitude:.5f}")
    except Exception as e:
        print(f"Error processing audio: {e}")


    return (in_data, pyaudio.paContinue)


class AudioHandler(object):
    def __init__(self):
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 4096
        self.p = None
        self.stream = None


        # High-pass filter parameters
        self.low_cutoff = 80.0
        self.high_cutoff = 300.0


        # Amplitude Threshold
        self.amplitude_threshold = 3.0


    def start(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  output=False,
                                  frames_per_buffer=self.CHUNK,
                                  stream_callback=audio_callback)


    def stop(self):
        self.stream.close()
        self.p.terminate()




# Main function to start audio streaming
def stream_audio():
    p = pyaudio.PyAudio()


    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=4096,
                    stream_callback=audio_callback)


    print("Streaming and processing audio. Press Ctrl+C to stop.")
    stream.start_stream()


    try:
        while stream.is_active():
            pass
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == "__main__":
    stream_audio()









