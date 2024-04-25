import pyaudio
import librosa
from scipy.signal import find_peaks
import numpy as np
from collections import Counter
import scipy.signal
import crepe
import keras
import keras.backend as K
from music21 import note
import os
import noisereduce as nr

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import tensorflow as tf

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


def midi_number_to_pitch(midi_number):
    n = note.Note()
    print(type(n))
    n.pitch.midi = midi_number
    return n.pitch.nameWithOctave


def audio_callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.float32)


    reduced_noise_audio = nr.reduce_noise(y=audio_data, sr=44100, stationary=True, n_jobs=-1)

   # Apply bandpass filter
    filtered_audio = butter_bandpass_filter(reduced_noise_audio, lowcut=80, highcut=7000, sr=44100)




    try:
        time, frequency, confidence, activation = crepe.predict(filtered_audio, 16000, step_size=50, viterbi=True)
        # K.clear_session()
       
        if len(confidence) > 0:
            best_idx = np.argmax(confidence)
            freq = frequency[best_idx]
            midi_number = librosa.hz_to_midi(freq)




            amplitude = np.sqrt(np.mean(filtered_audio**2))
            print(f"Pitch: {midi_number_to_pitch(midi_number)}, Frequency: {freq:.2f} Hz, Confidence: {confidence[best_idx]:.2f}, Amplitude: {amplitude:.5f}")
    except Exception as e:
        print(f"Error processing audio: {e}")




    return (in_data, pyaudio.paContinue)


# Main function to start audio streaming
def stream_audio():
    p = pyaudio.PyAudio()




    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=2048,
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