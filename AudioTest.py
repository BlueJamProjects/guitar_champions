import pyaudio
import wave
import librosa
import math
from scipy.signal import find_peaks
import numpy as np
from collections import Counter
import scipy.signal

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

def correct_octave_error(midi_number, audio_signal, sr):
    # Convert MIDI to frequency
    initial_freq = librosa.midi_to_hz(midi_number)
    
    # Check the energy around the initial frequency and its lower octave
    lower_octave_freq = initial_freq / 2
    energy_initial = get_energy_around_freq(audio_signal, sr, initial_freq)
    energy_lower_octave = get_energy_around_freq(audio_signal, sr, lower_octave_freq)
    
    # Correct the MIDI number if the lower octave has more energy
    if energy_lower_octave > energy_initial:
        corrected_midi_number = librosa.hz_to_midi(lower_octave_freq)
        return corrected_midi_number
    else:
        return midi_number

# Audio processing and MIDI/amplitude calculation
def audio_callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.float32)
    
    # Apply bandpass filter
    filtered_audio = butter_bandpass_filter(audio_data, lowcut=80, highcut=10000, sr=44100)
    
    # Convert to MIDI (note: this is simplified for demonstration and may need refinement for accurate pitch detection)
    try:
        cqt = librosa.cqt(filtered_audio, sr=44100, fmin=librosa.note_to_hz('C1'), n_bins=72, bins_per_octave=12)
        mag_cqt = np.abs(cqt)
        summed_mag = np.sum(mag_cqt, axis=1)
        predominant_bin = np.argmax(summed_mag)
        midi_number = librosa.hz_to_midi(librosa.core.cqt_frequencies(n_bins=72, fmin=librosa.note_to_hz('C1'), bins_per_octave=12)[predominant_bin])

        #midi_number = correct_octave_error(midi_number, filtered_audio, 44100)
        
        # Calculate amplitude
        amplitude = np.sqrt(np.mean(filtered_audio**2))
        
        print(f"MIDI Number: {midi_number:.2f}, Amplitude: {amplitude:.5f}")
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



