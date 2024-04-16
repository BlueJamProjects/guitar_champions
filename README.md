# guitar_champions
482 Capstone project

## Dataset Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip3 install librosa, music21, matplotlib, crepe, pygame, pygame_menu, pygame_aseprite_animation, pyaudio, keras, tensorflow
```

### Usage
```python
dataset = get_dataset(filter_by={})
```
Return a multidimensional array consisting of audio data, sample rate, and metadata in the first, second, and third indices, respectively. The metadata array contains the filename, pitch, MIDI, string, fret, type, average MFCCs (mfccs_mean), and MFCCs variance (mfccs_var).
