from Recognizer import recognizer
import os
import sys


def find_path(test, name):
    cwd = os.getcwd()
    if test == 1:
        audio_path = os.path.join(cwd, "../dataset/test/", name)
    else:
        audio_path = os.path.join(cwd, "../dataset/audio/", name)
    normalized_path = os.path.normpath(audio_path)
    
    return normalized_path


def main():
    if len(sys.argv) not in [2, 3]:
        print("Usage: ./test.py <filename or 'dataset'> [bpm]")
        sys.exit(1)

    filename = sys.argv[1]

    bpm = int(sys.argv[2]) if len(sys.argv) == 3 else 0

    if filename.lower() == "dataset":
        print("Processing dataset...")
        print("")
        dataset = recognizer.get_dataset()  
        test_dataset = recognizer(None, bpm)
        test_dataset.group_tester(dataset)
    else:
        
   
           
        if bpm > 0:
            path = find_path(1, filename)
            test = recognizer(path, bpm) 
            test.multiple_notes_tester()
        else:
            path = find_path(0, filename)
            test = recognizer(path, bpm) 
            test.single_note_tester()

if __name__ == "__main__":
    main()
