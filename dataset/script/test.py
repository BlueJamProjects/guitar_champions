from Recognizer import recognizer
import os

def find_path(name):
    
    cwd = os.getcwd()
    audio_path = os.path.join(cwd, "../audio/", name)
    normalized_path = os.path.normpath(audio_path)
    
    return normalized_path

path1 = find_path("song1.wav")
test1 = recognizer(path1, 0)
test1.single_note_tester()

# dataset = recognizer.get_dataset()
# test2 = recognizer(None, 0)
# test2.group_tester(dataset)

path3 = find_path("test1.wav")
test3 = recognizer(path3, 120)
test3.multiple_notes_tester()
