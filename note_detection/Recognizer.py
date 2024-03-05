import librosa
import json
import os
import numpy as np
from scipy.signal import find_peaks, butter, lfilter
from collections import Counter
import matplotlib.pyplot as plt
from music21 import note

class recognizer: 
    
    def __init__(self, audio_path=None, bpm=None):
        self.audio = None
        self.sr = None
        # Only load audio if a path is provided
        if audio_path is not None:
            self.audio, self.sr = librosa.load(audio_path)
        self.bpm = bpm   
        self.notes = []
        self.position = []
        self.spectral_centroids = 0
        self.total_time = 0
        self.overall_list = []
        
    def __str__(self):
        return f"{self.audio}({self.bpm}), {self.notes}"

    # Define the butterworth filter
    @staticmethod
    def butter_lowpass_filter(data, cutoff, fs, order=6):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        y = lfilter(b, a, data)
        return y
    
    def filtered_audio(self, audio, sr):
        spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
        self.spectral_centroids = spectral_centroids
        avg_centroid = np.mean(spectral_centroids)
        cutoff = 1500 if avg_centroid > 6000 else 200
        
        return self.butter_lowpass_filter(audio, cutoff, sr, order=6)

    @staticmethod
    def load_audio_from_file(audio_path):
        """Load audio data from a local file."""
        
        audio_data, sr = librosa.load(audio_path, sr=None)  
        return audio_data, sr   
    
    @staticmethod
    def get_dataset(filter_by=None):
        dataset = []
        """Fetch dataset based on metadata and optional filtering critera"""     
        cwd = os.getcwd()
        meta_path = os.path.join(cwd, "../dataset/metadata.json") 
        audio_path = os.path.join(cwd, "../dataset/audio")
        
        with open(meta_path, 'r') as file:
            metadata = json.load(file)
            
        for item in metadata:
            if filter_by and item.get(filter_by['key']) != filter_by['value']:
                continue
            audio_file_path = os.path.join(audio_path, item['filename'])
            audio_data, sr = recognizer.load_audio_from_file(audio_file_path)
            dataset.append((audio_data, sr, item))
        
        
        return dataset
    
    # Midi Number Detection
    def single_note_predictor(self, audio, sr):
        midi_list = []
        filtered_audio = self.filtered_audio(audio, sr)
        cqt = np.abs(librosa.cqt(filtered_audio, sr=sr))
        
        for i in range(cqt.shape[1]):
            frame = cqt[:, i]
            peaks = find_peaks(frame, height=0.01, distance=10)[0]

            if peaks.size > 0:
                for peak in peaks:
                    frequency = librosa.cqt_frequencies(n_bins=cqt.shape[0], fmin=32.7, bins_per_octave=12)[peak]
                    midi_number = librosa.hz_to_midi(frequency)
                    midi_list.append(midi_number)
                
                
        return midi_list        

    def multiple_note_predictor(self, duration):
        overall_list = []
        midi_numbers_list = []
        total_time = 0
        result = []
        t = 0

        filtered_data = self.filtered_audio(self.audio, self.sr)

        # Compute CQT on filtered data
        cqt = np.abs(librosa.cqt(filtered_data, sr=self.sr))
        result = []
        
        t = 0
        j = 0
        # Detect the peak of each time frame
        time_interval = len(self.audio) / self.sr / cqt.shape[1]
        for i in range(cqt.shape[1]):
            frame = cqt[:, i]

            peaks = find_peaks(frame, height=0.01, distance=10)[0]
            if peaks.size > 0:
                for peak in peaks:
                    frequency = librosa.cqt_frequencies(n_bins=cqt.shape[0], fmin=32.7, bins_per_octave=12)[peak]

                    midi_number = librosa.hz_to_midi(frequency)
                    midi_numbers_list.append(midi_number)
                    overall_list.append(midi_number)
            t += time_interval
            total_time += time_interval
            if t >= duration or i == range(cqt.shape[1])[-1]:
                j +=1
                result.append(midi_numbers_list)
                t = 0
                midi_numbers_list = []
        self.total_time = total_time
        self.overall_list = overall_list
        return result
    
    # Evaluator 
    def group_tester(self, dataset):
        score = 0
        self.notes = []  # Ensure this is clear; it should likely be outside the loop.
        self.position = []  # Same as above.
        for audio_data, sr, metadata in dataset:
            midi = metadata['midi']
            s = metadata["string"]
            f = metadata["fret"]
            self.notes.append((audio_data, midi, sr))
            self.position.append((s, f))
        
        for i in range(len(self.notes)):
            # Use self to call instance method correctly.
            midi_list = self.single_note_predictor(self.notes[i][0], self.notes[i][2])
            midi_counts = Counter(midi_list)
            if not midi_counts:
                continue
            
            midi = round(midi_counts.most_common(1)[0][0])
            if midi == self.notes[i][1]:
                score += 1
            else:
                print(f"Signal {i} is Incorrect: ")
                print("Prediction: ", midi)
                print("Expectation: ",self.notes[i][1])
                print("string: ", self.position[i][0], " fret: ", self.position[i][1])
                print("---------------------------")
                # print("avg_centroid: ", avg_centroid)     
        
        print(f"There are totally {len(self.notes)} notes detected")
        print(f"Accuracy Rate: {(score / len(self.notes)) * 100}%")
        
        return score / len(self.notes)

    def multiple_notes_tester(self):
        multi_midi = []
        multi_pitch = []
        r = self.multiple_note_predictor(60/self.bpm)
        print(len(r))

        for i in r:
            if i:
                midi_counts = Counter(i)
                most_common_midi = midi_counts.most_common(1)[0][0]
                midi_number = round(most_common_midi)
                pitch_name = midi_number_to_pitch(midi_number)
                
                multi_midi.append(midi_number)
                multi_pitch.append(pitch_name)
                

        # Illustate the midi numbers
        
        # plt.figure(figsize=(14, 6))
        # plt.plot(self.overall_list, marker='o', linestyle='-', markersize=4)
        # plt.ylabel('MIDI Number')
        # plt.xlabel('Time')
        # plt.title('MIDI Numbers Over Time')
        # plt.show()

        # Overall Result
        print(f"There are {len(r)} notes")
        print(f"Total time: {round(self.total_time)}s", )   
        print("Multi MIDI List: ", multi_midi)
        print("Multi Pitch List: ", multi_pitch)
        
    def single_note_tester(self):
        midi_list = self.single_note_predictor(self.audio, self.sr)
        midi_counts = Counter(midi_list)
        midi_number = round(midi_counts.most_common(1)[0][0])
        pitch_name = midi_number_to_pitch(midi_number)
        print(f"The midi number is {midi_number}")          
        print(f"MIDI number {midi_number} is {pitch_name}")
        
        # Illustate the midi numbers
        # plt.figure(figsize=(14, 6))
        # plt.plot(midi_list, marker='o', linestyle='-', markersize=4)
        # plt.ylabel('MIDI Number')
        # plt.xlabel('Time')
        # plt.title('MIDI Numbers Over Time')
        # plt.show()
    
def midi_number_to_pitch(midi_number):
    n = note.Note()
    n.pitch.midi = midi_number
    return n.pitch.nameWithOctave
    