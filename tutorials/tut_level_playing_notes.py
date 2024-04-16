import pygame

import os

import copy

# note recognition imports

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

from pygame_aseprite_animation import *

import helpers.settings_helper as settings_helper

import helpers.tutorial_info as tutorial_info

import partials.buttons.text_button as text_button

import partials.titlecard.title_card as title_card

import partials.tutorial_popup.tutorial_popup as tutorial_popup

import helpers.sprite_item as sprite_item

import partials.notes.text_note as note

from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    K_RIGHT,
    K_LEFT,
    KEYDOWN,
    QUIT,
    K_SPACE,
)

# For keeping track of the last 3 played midi numbers

main_midi_number_arr = [40, 40, 40]

def start():

    running = True
    paused = False
    restart_level = False

    pauserendered = False

    played_example_note8 = False

    user_settings = settings_helper.get_settings()

    # Define constants for the screen width and height
    SCREEN_WIDTH = pygame.display.get_surface().get_size()[0]
    SCREEN_HEIGHT = pygame.display.get_surface().get_size()[1]

    PLAY_LINE_LOCATION = 290


    # Setup for sounds, defaults are good
    pygame.mixer.init()

    # Initialize pygame
    pygame.init()

    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


    pause_title = title_card.Titlecard(text="   Paused   ", width= 350,height= 59, left_padding= SCREEN_WIDTH/2 - 175, top_padding= SCREEN_HEIGHT/2 - 180)
    

    # These are the buttons for the pause menu
    resume_button = text_button.TextButton(text=" Resume ", width= 96,height= 44, left_padding= SCREEN_WIDTH/2 - 50, top_padding= SCREEN_HEIGHT/2 - 80)
    restart_button = text_button.TextButton(text=" Restart ", width= 94,height= 44, left_padding= SCREEN_WIDTH/2 - 48, top_padding= SCREEN_HEIGHT/2 - 10)
    main_menu_button = text_button.TextButton(text=" Main Menu ", width= 128,height= 44, left_padding= SCREEN_WIDTH/2 - 62, top_padding= SCREEN_HEIGHT/2 +60)
    quit_button = text_button.TextButton(text=" Quit ", width= 60,height= 44, left_padding= SCREEN_WIDTH/2 -30, top_padding= SCREEN_HEIGHT/2 + 120)



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
    
    # TODO make the custom sprites for the tutorial
    # START/////////
    bg_img = pygame.image.load('assets/images/backgrounds/glacier_night.jpeg')
    bg_img = pygame.transform.scale(bg_img,(SCREEN_WIDTH,SCREEN_HEIGHT))

    #  the background image of the tabs
    tabs_image = pygame.image.load("assets/images/backgrounds/tabs_outline.png").convert()
    tabs_image.set_colorkey((255, 255, 255), RLEACCEL)

    # the image of the line where the ntoes should be when played
    play_line_image = pygame.image.load("assets/images/backgrounds/play_line.png").convert()
    play_line_image.set_colorkey((255, 255, 255), RLEACCEL)

    # set aseprite file directory
    dirname = os.path.dirname(__file__)
    aseprite_file_directory = 'assets/animations/rjgwgMOVINGHANDTOPLAY1.aseprite'

    #guitar guy animations
    test_animation = Animation(aseprite_file_directory)
    animationmanager = AnimationManager([test_animation], screen)
    strumAnimation = Animation('assets/animations/rjgwgSTRUMMINGGUITAR1.aseprite')
    animationmanager2 = AnimationManager([strumAnimation], screen)

    example_note1 = note.Note(text="0", midi=55, time_to_next_note=1, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0)
    example_note1.set_x_location(500)

    example_note2 = note.Note(text="0", midi=55, time_to_next_note=1, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0)
    example_note2.set_x_location(290)
    example_note2.set_active_color()

    example_note3 = note.Note(text="0", midi=55, time_to_next_note=1, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0)
    example_note3.set_x_location(210)
    example_note3.set_played_color()

    example_note4 = note.Note(text="0", midi=55, time_to_next_note=1, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0)
    example_note4.set_x_location(210)
    example_note4.set_missed_color()

    example_note5 = note.Note(text="0", midi=55, time_to_next_note=1, tab_line=1, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0)
    example_note5.set_x_location(500)
    example_note5.set_active_color()

    example_note6 = note.Note(text="0", midi=55, time_to_next_note=1, tab_line=6, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0)
    example_note6.set_x_location(500)
    example_note6.set_active_color()

    example_note7 = note.Note(text="1", midi=55, time_to_next_note=1, tab_line=6, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0)
    example_note7.set_x_location(500)
    example_note7.set_active_color()

    example_note8 = note.Note(text="1", midi=41, time_to_next_note=1, tab_line=6, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0)
    example_note8.set_x_location(290)
    example_note8.set_active_color()

    frames_since_note = 0

    # this is a multiplier that is used to figure out how many beats later the next note should come
    # after each note is created this is dynamically updated by calling a function on that note
    # 1.0 means that the next note plays one beat later, 2.0 is 2 beats later while 0.5 would be half a beat later
    time_to_next_note = 1.0

    Notes = pygame.sprite.Group()

    note_index = 0

    # This is the array with the song's note information
    song_notes = [
        note.Note(text="0", midi=64, time_to_next_note=1, tab_line=1, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0),
        note.Note(text="1", midi=65, time_to_next_note=1, tab_line=1, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=2),
        note.Note(text="2", midi=66, time_to_next_note=1, tab_line=1, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=4),
        note.Note(text="3", midi=67, time_to_next_note=2, tab_line=1, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=4),
       
        note.Note(text="0", midi=59, time_to_next_note=1, tab_line=2, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0),
        note.Note(text="1", midi=60, time_to_next_note=1, tab_line=2, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=2),
        note.Note(text="2", midi=61, time_to_next_note=1, tab_line=2, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=4),
        note.Note(text="3", midi=62, time_to_next_note=2, tab_line=2, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=4),
       
        note.Note(text="0", midi=55, time_to_next_note=1, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0),
        note.Note(text="1", midi=56, time_to_next_note=1, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=2),
        note.Note(text="2", midi=57, time_to_next_note=1, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=4),
        note.Note(text="3", midi=58, time_to_next_note=2, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=4),
       
        note.Note(text="0", midi=50, time_to_next_note=1, tab_line=4, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0),
        note.Note(text="1", midi=51, time_to_next_note=1, tab_line=4, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=2),
        note.Note(text="2", midi=52, time_to_next_note=1, tab_line=4, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=4),
        note.Note(text="3", midi=53, time_to_next_note=2, tab_line=4, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=4),
       
        note.Note(text="0", midi=45, time_to_next_note=1, tab_line=5, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0),
        note.Note(text="1", midi=46, time_to_next_note=1, tab_line=5, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=2),
        note.Note(text="2", midi=47, time_to_next_note=1, tab_line=5, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=4),
        note.Note(text="3", midi=48, time_to_next_note=2, tab_line=5, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=4),
       
        note.Note(text="0", midi=40, time_to_next_note=1, tab_line=6, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0),
        note.Note(text="1", midi=41, time_to_next_note=1, tab_line=6, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=2),
        note.Note(text="2", midi=42, time_to_next_note=1, tab_line=6, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=4),
        note.Note(text="3", midi=43, time_to_next_note=2, tab_line=6, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=4),
       
        ]

    complete_tutorial_button = text_button.TextButton(text=" Complete ", width= 96,height= 44, left_padding= SCREEN_WIDTH/2 - 50, top_padding= SCREEN_HEIGHT/2 - 80)
    

    curr_tutorial_info = tutorial_info.TutorialInfo(
         popup_list = [
            #   1
              tutorial_popup.TutorialPopup("Welcome to the Playing Notes tutorial! Press the next button on screen or use the arrow keys to navigate", left_padding=10, top_padding=20),
             #   2
              tutorial_popup.TutorialPopup("In this game, notes, like this will glide across the screen and you'll need to play them once they change to blue", left_padding=100, top_padding=20, show_hightlight_region=True, highlight_region_position=example_note1.rect),
            #   3
              tutorial_popup.TutorialPopup("When they change to Blue they'll look like this", left_padding=10, top_padding=250, show_hightlight_region=True, highlight_region_position=example_note2.rect),
             #   4
              tutorial_popup.TutorialPopup("If you play them correctly they'll change to Green", left_padding=10, top_padding=250, show_hightlight_region=True, highlight_region_position=example_note3.rect),
             #   5
              tutorial_popup.TutorialPopup("But if you play them incorrectly they'll change to Red", left_padding=10, top_padding=250, show_hightlight_region=True, highlight_region_position=example_note4.rect),
            #   6
              tutorial_popup.TutorialPopup("We are using tab notation to represent notes. So a note on the top line here would be played on the bottom string (This is called the first string).", left_padding=10, top_padding=20, show_hightlight_region=True, highlight_region_position=example_note5.rect),
            #   7
              tutorial_popup.TutorialPopup("While a note on the bottom line here would be played on the top string (This is called the 6th string).", left_padding=10, top_padding=250, show_hightlight_region=True, highlight_region_position=example_note6.rect),
            #   8
              tutorial_popup.TutorialPopup("The fret of the note is represented by its number. In this case the number is 0 which means you just pluck the string without pressing down a fret.", left_padding=10, top_padding=250, show_hightlight_region=True, highlight_region_position=example_note6.rect),
            #   9
              tutorial_popup.TutorialPopup("While for this one, the number is 1 which means you hold down the string at the first fret and then pluck the string", left_padding=10, top_padding=250, show_hightlight_region=True, highlight_region_position=example_note7.rect),
            
            #   10
              tutorial_popup.TutorialPopup("PLAY THIS NOTE! You'll press down your finger on the top string at the first fret and pluck the string. When it changes to green you've played it correctly.", left_padding=10, top_padding=20, show_hightlight_region=True, highlight_region_position=example_note8.rect, highlight_region_color=(0,0,0), trigger_effect_number=2,),
             #   11
              tutorial_popup.TutorialPopup("On the next screen you can practice playing notes as they come across the screen. Don't worry you can practice as long as you need. :)", left_padding=10, top_padding=20,),
            #   12
              tutorial_popup.TutorialPopup("THIS IS PRACTICE! Don't worry about missing notes :)", left_padding=10, top_padding=20, trigger_effect_number=3,),
            #   13
              tutorial_popup.TutorialPopup("Now, on the next screen you can practice playing different notes as they come across the screen. Don't worry you can practice as long as you need. :)", left_padding=10, top_padding=20, trigger_effect_number=5),
            #   14
              tutorial_popup.TutorialPopup("THIS IS PRACTICE! Don't worry about missing notes :)", left_padding=300, top_padding=400, trigger_effect_number=4,),
            #   15
              tutorial_popup.TutorialPopup("Now you're ready to try out a song!", left_padding=10, top_padding=20,trigger_effect_number=5),
            
            # END
            tutorial_popup.TutorialPopup("Press complete to finish the tutorial", top_padding= 220, left_padding= 20, trigger_effect_number=1,),


              ],
         sprites_list = [
            # 1
              [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                   
                   ],
                   # 2
              [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite= example_note1.surf, location=example_note1.rect),
                   
                   ],
                   # 3
              [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite= example_note2.surf, location=example_note2.rect),
                   
                   ],
                   # 4
              [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite= example_note3.surf, location=example_note3.rect),
                   
                   ],
                   # 5
              [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite= example_note4.surf, location=example_note4.rect),
                   
                   ],
                #    6
                [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite= example_note5.surf, location=example_note5.rect),
                   
                   ],
                #    7
                [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite= example_note6.surf, location=example_note6.rect),
                   
                   ],
                    #    8
                [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite= example_note6.surf, location=example_note6.rect),
                   
                   ],

                     #    9
                [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite= example_note7.surf, location=example_note7.rect),
                   
                   ],


                    #    10
                [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite= example_note8.surf, location=example_note8.rect),
                   
                   ],

                   #    11
                [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                  
                   
                   ],

                   #    12
                [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                  
                   
                   ],

                   #    13
                [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                  
                   
                   ],

                    #     14
                [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                  
                   
                   ],

                   #     15
                [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                  
                   
                   ],


                   # END
              [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                   sprite_item.SpriteItem(sprite= complete_tutorial_button.render, location=complete_tutorial_button.button_position)
                   ],

         ],
    )


    # END/////////

    current_popup = curr_tutorial_info.current_popup

   
    current_sprites = curr_tutorial_info.current_sprites

    
    
    


    # The main loop
    while running:

        # PAUSED LOOP
        if paused == True:
              
            for event in pygame.event.get():

                # Did the user hit a key?
                if event.type == KEYDOWN:

                    # Was it the Escape key? If so, stop the loop
                    if event.key == K_ESCAPE or event.key == K_SPACE:
                        paused = False
                        

                    # Did the user click the window close button? If so, exit
                    elif event.type == QUIT:
                        os._exit(status=0)


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
                        os._exit(status=0)



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
        

        # NON-PAUSED LOOP

        else:

            
            current_popup = curr_tutorial_info.current_popup
            current_sprites = curr_tutorial_info.current_sprites



            if (current_popup.trigger_effect_number == 2):
                                    

                                    if (example_note8.check_correct_note(main_midi_number_arr)):
                                        # print("Correct note was played")
                                        played_example_note8 = True


                                    if(played_example_note8 == True):
                                        example_note8.set_played_color()
                                        current_sprites = [
                                            sprite_item.SpriteItem(sprite = bg_img, location = (0,0)),
                                            sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                                            sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                                            sprite_item.SpriteItem(sprite= example_note8.surf, location=example_note8.rect),
                                            ]
                                        
            if (current_popup.trigger_effect_number == 5):
                Notes = pygame.sprite.Group()
                note_index = 0
                                        
            if (current_popup.trigger_effect_number == 3 or current_popup.trigger_effect_number == 4):
                # This adds notes every second
                # This uses the current fps so that you are adding notes accurately
                if frames_since_note >= ((clock.get_fps() * time_to_next_note )// 1) and (clock.get_fps() > 0.1):
                        frames_since_note = 0

                        if (current_popup.trigger_effect_number == 3):
                            new_Note = note.Note(text="1", midi=41, time_to_next_note=2.0, tab_line=6, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0)
                            time_to_next_note = 4.0
                        if (current_popup.trigger_effect_number == 4):
                            # This ensures that this makes the note a deep copy
                            new_Note = note.Note(text=song_notes[note_index].text, midi=song_notes[note_index].midi, time_to_next_note=song_notes[note_index].time_to_next_note, tab_line=song_notes[note_index].tab_line, Screen_Width=song_notes[note_index].Screen_Width, Screen_Height=song_notes[note_index].Screen_Height, id=song_notes[note_index].id),
        
                            time_to_next_note = song_notes[note_index].get_time_to_next_note()
                            # print("Current note index")
                            # print(note_index)
                            if (note_index < len(song_notes)-1):
                                note_index = note_index + 1
                            else:
                                note_index = 0


                        Notes.add(new_Note)
                        # print("Added a new note")
                        
                       
                frames_since_note += 1

                Notes.update()
                # print("Notes were updated")
                for curr_note in Notes:
                    # print("For each note")
                    # This loops through all the notes on screen
                    if abs((PLAY_LINE_LOCATION-200) - curr_note.get_x_location()) < 20:

                        # This triggers if the note is the one on screen
                        # This is a function from the note that we check to see if it's key was the one pressed
                        # print("MIDI Number: ",main_midi_number)
                        if curr_note.check_correct_note(main_midi_number_arr):
                            curr_note.was_played=True
                            # print("Correct note played")
                            
                        
                    if (abs(PLAY_LINE_LOCATION - curr_note.get_x_location()) < 25) :
                                    # it checks to see if the note is close enough to the play line to update
                                    
                                    

                        if curr_note.get_is_active() == False:
                            # if the note is currently note active
                            curr_note.set_active_color()


                    else:
                         if curr_note.get_is_active() == True:
                            # if it is leaving the play line regio
                            if((curr_note.get_x_location() < (PLAY_LINE_LOCATION - 200))):
                                if curr_note.get_was_played() == True:
                                    # if note was played successfully
                                    curr_note.set_played_color()
                                else:
                                    # if the note was not played successfully
                                    curr_note.set_missed_color()
                                

                

            for event in pygame.event.get():

                            # Did the user hit a key?
                            if event.type == KEYDOWN:

                                # Was it the Escape key? If so, stop the loop
                                if event.key == K_ESCAPE or event.key == K_SPACE:
                                    paused = True
                                    pauserendered = False
                                    # print("paused the game")

                                elif event.key == K_RIGHT:
                                    if (current_popup.trigger_effect_number == 3 or current_popup.trigger_effect_number == 4):
                                        Notes = pygame.sprite.Group()
                                        curr_tutorial_info.sprites_list[curr_tutorial_info.sprites_index] = [
                                        sprite_item.SpriteItem(sprite = bg_img, location = (0,0)),
                                        sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                                        sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)), 
                                        ]
                                     
                                     # TODO Add custom next code here
                                    # START/////////
                                    # if current_popup.trigger_effect_number == 1:
                                        # print("Trigger effect 1")

                                    # END/////////
                                    curr_tutorial_info.next()
                                    

                                elif event.key == K_LEFT:
                                    # TODO Add custom previous code here
                                    # START/////////
                                    if (current_popup.trigger_effect_number == 3 or current_popup.trigger_effect_number == 4):
                                        Notes = pygame.sprite.Group()
                                        curr_tutorial_info.sprites_list[curr_tutorial_info.sprites_index] = [
                                        sprite_item.SpriteItem(sprite = bg_img, location = (0,0)),
                                        sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                                        sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)), 
                                        ]

                                    # END/////////
                                    curr_tutorial_info.previous()

                            # Did the user click the window close button? If so, exit
                            elif event.type == QUIT:
                                os._exit(status=0)

                            # Here we check for hover events 
                            if event.type==pygame.MOUSEMOTION:
                                current_popup.button_on_hover()

                                # TODO Add the hover effects for this tutorials example buttons
                                # START/////////
                                
                                complete_tutorial_button.on_hover()
                                # END/////////
                                
                        

                            # Here we check for clicks events 
                            if event.type==pygame.MOUSEBUTTONDOWN:

                                # text_buttons should be pressed like this
                                if (current_popup.button_is_pressed() == True):
                                    # print("Current popup pressed")
                                    if (current_popup.trigger_effect_number == 3 or current_popup.trigger_effect_number == 4):
                                        Notes = pygame.sprite.Group()
                                        curr_tutorial_info.sprites_list[curr_tutorial_info.sprites_index] = [
                                        sprite_item.SpriteItem(sprite = bg_img, location = (0,0)),
                                        sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                                        sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)), 
                                        ]
                                    curr_tutorial_info.next()

                                    # TODO Add custom next code here
                                    # START/////////

                                    # if current_popup.trigger_effect_number == 1:
                                    #     print("Trigger effect 1")

                                    # END/////////


                                 # TODO Add the click effects for this tutorials example buttons
                                    # START/////////
                                        # you should make certain you're on the correct screen before allowing the button to be pressed

                                

                                if (current_popup.trigger_effect_number == 1):
                                    if (complete_tutorial_button.is_pressed() == True):
                                        running = False

                                

                                        
                                # END/////////
            

            if (current_popup.trigger_effect_number == 3 or current_popup.trigger_effect_number == 4):
                for entity in Notes:
                    current_sprites.append(sprite_item.SpriteItem(sprite=entity.surf, location=entity.rect))

            
            for curr_sprite_item in current_sprites:
                if curr_sprite_item.is_box == True:
                    # If the current sprite is a box

                    if curr_sprite_item.box_has_border == True:
                        #  If the box does have a border
                        pygame.draw.rect(screen,curr_sprite_item.box_color,curr_sprite_item.box_rect, curr_sprite_item.box_border)
                    else:
                        # If the box has no border
                        pygame.draw.rect(screen,curr_sprite_item.box_color,curr_sprite_item.box_rect)
                else:
                    # If the current sprite is not a box
                    screen.blit(curr_sprite_item.sprite, curr_sprite_item.location)
                    if curr_sprite_item.is_background == True:
                        # load tutorial box frame
                        tutframe = pygame.image.load('assets/images/backgrounds/frame.png')
                        tutframe.set_alpha(140)
                        tutframe=pygame.transform.scale(tutframe,(381,360))
                        screen.blit(tutframe,(current_popup.outline_position.x-46,current_popup.outline_position.y-70))




            # TODO This is the animation of the player
            animationmanager2.update_self(30, 390)

            

            pygame.draw.rect(screen,current_popup.outline_color,current_popup.outline_position)

            screen.blit(current_popup.line1_render, current_popup.line1_position)
            screen.blit(current_popup.line2_render, current_popup.line2_position)
            screen.blit(current_popup.line3_render, current_popup.line3_position)
            screen.blit(current_popup.line4_render, current_popup.line4_position)
            screen.blit(current_popup.line5_render, current_popup.line5_position)

            screen.blit(current_popup.number_render, current_popup.number_position)
            pygame.draw.rect(screen,(209,129,0),current_popup.button_position)
            screen.blit(current_popup.button_render, current_popup.button_position)
            pygame.draw.rect(screen,(255,255,255),current_popup.button_position, 2)

            if (current_popup.show_hightlight_region == True):
                pygame.draw.rect(screen,current_popup.highlight_region_color,current_popup.highlight_region_position.scale_by(1.4), 5)

            


            pygame.display.update()
            clock.tick_busy_loop(30)


    # print("Exiting")
    # print(restart_level)
     # Stop Audio
    stream.stop_stream()
    stream.close()
    p.terminate()

    # At this point, we're done, so we can stop and quit the mixer
    pygame.mixer.music.stop()
    pygame.mixer.quit()

   
    

    # If the level should be restarted the restart it
    if restart_level == True:
        # print("Restart level was true")
        start()

    # print("This happened")
    # return




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