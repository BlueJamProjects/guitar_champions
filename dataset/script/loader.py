import requests
import json
import librosa
import os

def load_audio_from_file(audio_path):
    """Load audio data from a local file."""
    audio_data, sr = librosa.load(audio_path, sr=None)  
    return audio_data, sr

def get_dataset(filter_by=None):
    """Fetch dataset based on metadata and optional filtering criteria."""
    cwd = os.getcwd()
    meta_path = os.path.join(cwd, '../metadata.json')
    audio_path = os.path.join(cwd, '../audio')
    with open(meta_path, 'r') as file:
        metadata = json.load(file)    
        dataset = []
        
    for item in metadata:
        if filter_by and item.get(filter_by['key']) != filter_by['value']:
            continue  
        audio_file_path = os.path.join(audio_path, item['filename'])
        audio_data, sr = load_audio_from_file(audio_file_path)
        dataset.append((audio_data, sr, item))
    
    return dataset
