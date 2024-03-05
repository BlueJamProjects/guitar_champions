import os
import json
import librosa
import numpy as np
import pandas as pd
from music21 import note

def pitch_to_midi_music21(pitch):
    n = note.Note(pitch)
    return n.pitch.midi

# Path to the folder containing your audio files
script_dir = os.path.dirname(os.path.realpath(__file__))
folder_path = os.path.join(script_dir, '../dataset/audio')
# List all files in the folder
filenames = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
# Initialize the metadata list
metadata = []

for filename in filenames:
    # Ensure the file is a .wav file
    if filename.endswith('.wav'):
        # Get the path to the file
        file_path = os.path.join(folder_path, filename)
        
        # Load the audio file
        audio, sr = librosa.load(file_path, sr=None)
        
        # Extract MFCCs
        mfccs = librosa.feature.mfcc(y=audio, sr=sr)
        mfccs_mean = np.mean(mfccs, axis=1)
        
        # MFCCs variance
        mfccs_var = np.var(mfccs, axis=1)
        
        # Convert MFCCs to a list 
        mfccs_mean_list = mfccs_mean.tolist()
        mfccs_var_list = mfccs_var.tolist()
        
        # Split the filename to extract pitch, string, and fret
        name_parts = filename.split('.')[0].split('_')  
        pitch = name_parts[0]
        midi = pitch_to_midi_music21(pitch)
        string_number = int(name_parts[1][0])  
        fret_number = int(name_parts[1][1:])  

        # Append this information as a dictionary to the metadata 
        metadata.append({
            "filename": filename,
            "pitch": pitch,
            "midi": midi,
            "string": string_number,
            "fret": fret_number,
            "type": "classical",
            "mfccs_mean": mfccs_mean_list,
            "mfccs_var": mfccs_var_list
        })

# Convert metadata list to JSON and save to a file
with open('metadata.json', 'w') as file:
    json.dump(metadata, file, indent=4)

print("Metadata JSON file has been created.")
