# import pygame asprite package, download by typing "pip3 install pygame_aseprite_animation" into your terminal
from pygame_aseprite_animation import *
# Import the pygame module
import os, pygame

# Import random for random numbers
import random

import sys
import matplotlib.pyplot as plt
import pyaudio
import wave
import librosa
import math
from scipy.signal import find_peaks
import numpy as np
from collections import Counter
import scipy.signal


import crepe
import keras
import keras.backend as K
from music21 import note as music21Note

os.environ['CUDA_VISIBLE_DEVICS'] = '-1'

import tensorflow as tf

# Import the menu library to more easily make menu selction
import pygame_menu
 
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

import partials.player.playing_player as playing_player
import partials.notes.text_note as note
import partials.buttons.text_button as text_button

import helpers.settings_helper as settings_helper

import partials.titlecard.title_card as title_card


main_midi_number_arr = [40, 40, 40]

def start():


    user_settings = settings_helper.get_settings()

    # Define constants for the screen width and height
    SCREEN_WIDTH = pygame.display.get_surface().get_size()[0]
    SCREEN_HEIGHT = pygame.display.get_surface().get_size()[1]

    PLAY_LINE_LOCATION = 290

    # Variable to keep our main loop running
    running = True
    paused = False
    completed = False
    restart_level = False
    pauserendered=False


    # Setup for sounds, defaults are good
    pygame.mixer.init()

    # Initialize pygame
    pygame.init()

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()

    # this keeps track of how many frames have occured since the last note was sent out
    # it is used later for keeping the notes sending at a regular rate
    frames_since_note = 0

    if user_settings.enable_metronome == True:
        # Load and play our background music
        pygame.mixer.music.load("assets/sounds/background-music/metro-34-60bpm.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(user_settings.volume / 100)


    # Create our 'player'
    player = playing_player.Player(top_padding=390)

    

    # Create groups to hold Note sprites, and all sprites
    # - Notes is used for position updates
    # - all_sprites isused for rendering
    Notes = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)


    # Start Audio
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=2048,
                    stream_callback=audio_callback)

    print("Streaming and processing audio. Press Ctrl+C to stop.")
    stream.start_stream()


    # Create the background image for the level
    bg_img = pygame.image.load('assets/images/backgrounds/happy_birthday_background.png')
    bg_img = pygame.transform.scale(bg_img,(SCREEN_WIDTH,SCREEN_HEIGHT))

    # a foreground image for the notes to go behind
    fg_image = pygame.image.load("assets/images/backgrounds/happy_birthday_foreground.png").convert()
    fg_image.set_colorkey((255, 255, 255), RLEACCEL)


    # the background image of the tabs
    tabs_image = pygame.image.load("assets/images/backgrounds/tabs_outline.png").convert()
    tabs_image.set_colorkey((255, 255, 255), RLEACCEL)

    # the image of the line where the ntoes should be when played
    play_line_image = pygame.image.load("assets/images/backgrounds/play_line.png").convert()
    play_line_image.set_colorkey((255, 255, 255), RLEACCEL)

    


    # This is the background for the final screen
    score_screen_background = pygame.image.load('assets/images/backgrounds/orange_background.jpg').convert()
    score_screen_background.set_colorkey((255, 255, 255), RLEACCEL)

    end_screen_cheems = pygame.image.load('assets/images/characters/npcs/birthday_dog.png')

    completed_restart_level_button = text_button.TextButton(text=" Restart Level ", width= 151,height= 44, left_padding= SCREEN_WIDTH/2 + 175, top_padding= SCREEN_HEIGHT/2 + 50)

    complete_level_button = text_button.TextButton(text=" Return to Menu ", width= 177,height= 44, left_padding= SCREEN_WIDTH/2 + 163, top_padding= SCREEN_HEIGHT/2 + 140)

    

    # This is the transparent background for the pause menu
    transparent_surface = pygame.Surface((SCREEN_WIDTH -60, SCREEN_HEIGHT - 60), pygame.SRCALPHA)
    transparent_surface.fill((255,255,255, 10))
    pygame.Surface.set_alpha(transparent_surface, 255)
    
    pause_title = title_card.Titlecard(text="   Paused   ", width= 350,height= 59, left_padding= SCREEN_WIDTH/2 - 175, top_padding= SCREEN_HEIGHT/2 - 180)
    
    # These are the buttons for the pause menu
    resume_button = text_button.TextButton(text=" Resume ", width= 96,height= 44, left_padding= SCREEN_WIDTH/2 - 50, top_padding= SCREEN_HEIGHT/2 - 80)
    restart_button = text_button.TextButton(text=" Restart ", width= 94,height= 44, left_padding= SCREEN_WIDTH/2 - 48, top_padding= SCREEN_HEIGHT/2 - 10)
    main_menu_button = text_button.TextButton(text=" Main Menu ", width= 128,height= 44, left_padding= SCREEN_WIDTH/2 - 62, top_padding= SCREEN_HEIGHT/2 +60)
    quit_button = text_button.TextButton(text=" Quit ", width= 60,height= 44, left_padding= SCREEN_WIDTH/2 -30, top_padding= SCREEN_HEIGHT/2 + 120)



    # Variables to keep track of the notes of the song
    note_index = 0

    # this is a multiplier that is used to figure out how many beats later the next note should come
    # after each note is created this is dynamically updated by calling a function on that note
    # 1.0 means that the next note plays one beat later, 2.0 is 2 beats later while 0.5 would be half a beat later
    time_to_next_note = 1.0
 

    # This is the array with the song's note information
    song_notes = [
        note.Note(text="0", midi=55, time_to_next_note=1, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0),
        note.Note(text="0", midi=55, time_to_next_note=1, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=1),
        note.Note(text="2", midi=57, time_to_next_note=1, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=2),
        note.Note(text="0", midi=55, time_to_next_note=1, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=3),
        note.Note(text="1", midi=60, time_to_next_note=1, tab_line=2, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=4),
        note.Note(text="0", midi=59, time_to_next_note=2.0, tab_line=2, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=5),

        note.Note(text="0", midi=55, time_to_next_note=0.5, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=6),
        note.Note(text="0", midi=55, time_to_next_note=0.5, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=7),
        note.Note(text="2", midi=57, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=8),
        note.Note(text="0", midi=55, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=9),
        note.Note(text="3", midi=62, tab_line=2, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=10),
        note.Note(text="1", midi=60, time_to_next_note=2.0, tab_line=2, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=11),


        note.Note(text="0", midi=55, time_to_next_note=0.5, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=13),
        note.Note(text="0", midi=55, time_to_next_note=0.5, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=14),
        note.Note(text="3", midi=67, tab_line=1, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=15),
        note.Note(text="0", midi=64, tab_line=1, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=16),
        note.Note(text="1", midi=60, tab_line=2, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=17),
        note.Note(text="0", midi=59, tab_line=2, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=18),
        note.Note(text="2", midi=57, time_to_next_note=2.0, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=19),

        note.Note(text="1", midi=65, time_to_next_note=0.5, tab_line=1, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=20),
        note.Note(text="1", midi=65, time_to_next_note=0.5, tab_line=1, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=21),
        note.Note(text="0", midi=64, tab_line=1, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=22),
        note.Note(text="1", midi=60, tab_line=2, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=23),
        note.Note(text="3", midi=62, tab_line=2, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=24),
        note.Note(text="1", midi=60, tab_line=2, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=25),
        ]
    
    # This keeps track of all the notes the player correctly hit
    # It is used for scoring at the end of the game
    correctly_played_notes = []
    

    # Our main loop
    while running:
        if completed == True:
        #    What should display if the game is over
            # Game over control loop
            
            pygame.mixer.music.stop()



            for event in pygame.event.get():

                    # Did the user hit a key?
                    if event.type == KEYDOWN:

                        # Was it the Escape key? If so, stop the loop
                        if event.key == K_ESCAPE:
                            running = False

                    # Did the user click the window close button? If so, exit
                    elif event.type == QUIT:
                        exit()

                    # Here we check for hover events 
                    if event.type==pygame.MOUSEMOTION:
                        complete_level_button.on_hover()
                        completed_restart_level_button.on_hover()
                        

                    # Here we check for clicks events 
                    if event.type==pygame.MOUSEBUTTONDOWN:

                        # text_buttons should be pressed like this
                        if (complete_level_button.is_pressed() == True):
                            running = False
                        
                        if (completed_restart_level_button.is_pressed() == True):
                            # this will exit the main loop, setting the condition to restart the level as true
                            restart_level = True
                            running = False

            # calculates the total of the notes that were correctly played
            total_score = len(correctly_played_notes)
            # create an array that stores accuracy percentage at each note
            accuracy_array=[]
            index_array=[]
            correcters=0
            totnote=0
            for noe in song_notes:
                if noe.was_played:
                    correcters+=1
                totnote+=1
                index_array.append(totnote)
                accuracy_array.append(correcters/totnote*100)
            plt.plot(index_array,accuracy_array, color='orange', linewidth=5)
            plt.ylim(0,100)
            plt.xlim(1,totnote)
            plt.title('Your overall Accuracy!')
            font = {'family' : 'normal',
                'weight' : 'bold',
                'size'   : 22}
            plt.yticks(fontsize=20)
            plt.xticks(fontsize=20)
            plt.rc('font', **font)
            plt.savefig('assets/images/tempgraphs/graphy.png')
            endplot = pygame.image.load('assets/images/tempgraphs/graphy.png')
            # create a font to select font and size
            score_font = pygame.font.Font('assets/font/BITSUMIS.ttf', 32)
            end_font=  pygame.font.Font('assets/font/Signatra.ttf', 80)
            # create a text surface object using the font
            # on which text is drawn on it.
            end_text= " Level  Complete! "
            end_render = end_font.render(end_text, False, (255, 255, 255), (239,159,20))
            score_font_text = " You correctly played: " 
            score_font_text2=" "+str(total_score) +" out of " + str(len(song_notes))+"! "
            score_font_render = score_font.render(score_font_text, False, (255, 255, 255), (239,159,20))
            score_font_render2 = score_font.render(score_font_text2, False, (255, 255, 255), (239,159,20))

            

            # This is calculates the player's percentage score
            percent_score = (total_score / len(song_notes)) * 100

            # this is the encouragement that shows up depending on their score
            encouragement_font_text = ""

            # this determines your encouragement method
            if percent_score == 100.0:
                encouragement_font_text = " Perfect! "
            elif percent_score >= 66.666:
                encouragement_font_text = " Well done! "
            elif percent_score >= 33.333:
                encouragement_font_text = " Good try! "
            else:
                encouragement_font_text = " You can do it! "


            encouragement_font_render = score_font.render(encouragement_font_text, False, (255, 255, 255), (239,159,20))


            # displays the visual elements of the completed screen
            screen.blit(score_screen_background,(0,0))
            s = pygame.Surface((SCREEN_WIDTH*.6,.9*SCREEN_HEIGHT)) 
            s.set_alpha(160)                
            s.fill((30,30,30))           
            screen.blit(s, (20,20))
            end_screen_cheems=pygame.transform.scale(end_screen_cheems,(270,270))
            endplot=pygame.transform.scale(endplot,(440,247))
            screen.blit(end_screen_cheems,(SCREEN_WIDTH-290,40))
            screen.blit(endplot,(SCREEN_WIDTH/2-360,300))
            screen.blit(score_font_render, (SCREEN_WIDTH/4-162,150))
            screen.blit(score_font_render2, (SCREEN_WIDTH/4-60,200))
            screen.blit(end_render, (SCREEN_WIDTH/4-130,50))
            pygame.draw.rect(screen,(255,255,255),pygame.Rect(SCREEN_WIDTH/4-130,50,373,85),2)
            screen.blit(encouragement_font_render, (SCREEN_WIDTH/4-75,250))
            screen.blit(completed_restart_level_button.render, completed_restart_level_button.button_position)
            pygame.draw.rect(screen,(255,255,255),completed_restart_level_button.button_position,2)
            screen.blit(complete_level_button.render, complete_level_button.button_position)
            pygame.draw.rect(screen,(255,255,255),complete_level_button.button_position,2)
            
            

            os.remove('assets/images/tempgraphs/graphy.png')
            pygame.display.update()
            clock.tick_busy_loop(30)

        else:
            # If we have started going through the notes and deleted the last one then the song is complete
            if note_index >= (len(song_notes) - 1):
                if len(Notes) == 0:
                    completed = True


            if paused == True:
                # The control loop for when the game is paused

                # pauses the game music
                pygame.mixer.music.pause()

                # cycles through every event and deals with them
                for event in pygame.event.get():

                    # Did the user hit a key?
                    if event.type == KEYDOWN:

                        # Was it the Escape key? If so, stop the loop
                        if event.key == K_ESCAPE:
                            pygame.mixer.music.unpause()
                            paused = False
                            pauserendered=False

                    # Did the user click the window close button? If so, exit
                    elif event.type == QUIT:
                        exit()

                    # Here we check for hover events 
                    if event.type==pygame.MOUSEMOTION:
                        resume_button.on_hover()
                        restart_button.on_hover()
                        main_menu_button.on_hover()
                        quit_button.on_hover()

                    # Here we check for clicks events 
                    if event.type==pygame.MOUSEBUTTONDOWN:

                        # text_buttons should be pressed like this
                        if (resume_button.is_pressed() == True):
                            paused = False
                            pygame.mixer.music.unpause()

                        elif(restart_button.is_pressed() == True):
                            restart_level = True
                            running = False

                        elif(main_menu_button.is_pressed() == True):
                            running = False

                        elif(quit_button.is_pressed() == True):
                            exit()

                #checks if pausemenu has been rendered once before and if not, draws the transparent background
                if(not pauserendered):
                    s = pygame.Surface((SCREEN_WIDTH/2,3*SCREEN_HEIGHT/4)) 
                    s.set_alpha(140)                
                    s.fill((239,159,20))           
                    screen.blit(s, (SCREEN_WIDTH/4,SCREEN_HEIGHT/8))
                    pauserendered=True

                #border around entire pause menu
                pygame.draw.rect(screen,(255,255,255),pygame.Rect(SCREEN_WIDTH/4,SCREEN_HEIGHT/8,SCREEN_WIDTH/2,3*SCREEN_HEIGHT/4),5)  

                # This visually updates the buttons on the pause screen and draws borders around them on render
                screen.blit(pause_title.render, pause_title.button_position)  
                pygame.draw.rect(screen,(0,0,0),pause_title.button_position,3)  

                screen.blit(resume_button.render, resume_button.button_position)
                pygame.draw.rect(screen,(255,255,255),resume_button.button_position,2)

                screen.blit(restart_button.render, restart_button.button_position)
                pygame.draw.rect(screen,(255,255,255),restart_button.button_position,2)

                screen.blit(main_menu_button.render, main_menu_button.button_position)
                pygame.draw.rect(screen,(255,255,255),main_menu_button.button_position,2)
                
                screen.blit(quit_button.render, quit_button.button_position)
                pygame.draw.rect(screen,(255,255,255),quit_button.button_position,2)

                pygame.display.update()
                clock.tick_busy_loop(30)

    

            else:


                for curr_note in Notes:
                    # This loops through all the notes on screen
                    if abs((PLAY_LINE_LOCATION-200) - curr_note.get_x_location()) < 20:

                        # This triggers if the note is the one on screen
                        # This is a function from the note that we check to see if it's key was the one pressed
                        # print("MIDI Number: ",main_midi_number)
                        if curr_note.check_correct_note(main_midi_number_arr):
                            curr_note.was_played=True
                            print("Correct note played")
                            correctly_played_notes.append(curr_note)
                            
                        #else:

                            # If a key was pressed on time but was incorrect
                            #print("Incorrect note played")9


                # Look at every event in the queue
                for event in pygame.event.get():

                    # Did the user hit a key?
                    if event.type == KEYDOWN:
                        
                        # Was it the Escape key? If so, pause the loop
                        if event.key == K_ESCAPE:
                            paused = True
                            pauserendered=False

                    

                    # Did the user click the window close button? If so, exit
                    elif event.type == QUIT:
                        exit()


                for curr_note in Notes:
                                # This loops through all the notes on screen

                                
                                

                                if (abs(PLAY_LINE_LOCATION - curr_note.get_x_location()) < 25) :
                                    # it checks to see if the note is close enough to the play line to update
                                    
                                    

                                    if curr_note.get_is_active() == False:
                                        # if the note is currently note active
                                        curr_note.set_active_color()


                                else:
                                     if curr_note.get_is_active() == True:
                                        # if it is leaving the play line region

                                        if((curr_note.get_x_location() < (PLAY_LINE_LOCATION - 200))):

                                            if curr_note.get_was_played() == True:
                                                # if note was played successfully
                                                curr_note.set_played_color()
                                            else:
                                                # if the note was not played successfully
                                                curr_note.set_missed_color()
                                    


                # This adds notes every second
                # This uses the current fps so that you are adding notes accurately
                if frames_since_note >= ((clock.get_fps() * time_to_next_note )// 1) and (clock.get_fps() > 0.1):
                        frames_since_note = 0

                        # Create the new Note, and add it to our sprite groups
                        if note_index < (len(song_notes)):

                            new_Note = song_notes[note_index]
                            note_index += 1
                            Notes.add(new_Note)

                            all_sprites.add(new_Note)

                            # global time_to_next_note
                            time_to_next_note = new_Note.get_time_to_next_note()
                       
                frames_since_note += 1

                # Get the set of keys pressed and check for user input
                pressed_keys = pygame.key.get_pressed()
                player.update(pressed_keys)


                # Update the position of our Notes
                Notes.update()


                # Fill the screen with the background image
                screen.blit(bg_img,(0,0))
                screen.blit(play_line_image,(0,0))
                screen.blit(fg_image, (0,0))
                screen.blit(tabs_image,(0,0))


                # Draw all our sprites
                for entity in all_sprites:
                    screen.blit(entity.surf, entity.rect)


                # Flip everything to the display
                pygame.display.flip()

                # Ensure we maintain a 30 frames per second rate
                clock.tick_busy_loop(30)


    # Stop Audio
    stream.stop_stream()
    stream.close()
    p.terminate()

    # At this point, we're done, so we can stop and quit the mixer
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    

    # If the level should be restarted the restart it
    if restart_level == True:
        start()



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
    n = music21Note.Note()
    n.pitch.midi = midi_number
    return n.pitch.nameWithOctave

def audio_callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.float32)


    # Apply bandpass filter
    filtered_audio = butter_bandpass_filter(audio_data, lowcut=80, highcut=7000, sr=16000)


    try:
        time, frequency, confidence, activation = crepe.predict(filtered_audio, 16000, step_size=50, viterbi=True)
        # K.clear_session()
       
        if len(confidence) > 0:
            best_idx = np.argmax(confidence)
            freq = frequency[best_idx]
            midi_number = librosa.hz_to_midi(freq)

            global main_midi_number_arr
            main_midi_number_arr.append(round(midi_number))
            main_midi_number_arr.pop(0)


            amplitude = np.sqrt(np.mean(filtered_audio**2))
            print(f"Pitch: {midi_number_to_pitch(midi_number)}, Frequency: {freq:.2f} Hz, Confidence: {confidence[best_idx]:.2f}, Amplitude: {amplitude:.5f}")
    except Exception as e:
        print(f"Error processing audio: {e}")


    return (in_data, pyaudio.paContinue)

    

