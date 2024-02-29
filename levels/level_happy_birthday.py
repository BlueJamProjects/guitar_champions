# import pygame asprite package, download by typing "pip3 install pygame_aseprite_animation" into your terminal
from pygame_aseprite_animation import *
# Import the pygame module
import os, pygame

# Import random for random numbers
import random

import sys


# Import the menu library to more easily make menu selction
import pygame_menu
 
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    RLEACCEL,
    K_a,
    K_b,
    K_c,
    K_d,
    K_e,
    K_f,
    K_g,
    K_0,
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_6,
    K_7,
    K_8,
    K_9,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

import partials.player.playing_player as playing_player
import partials.notes.text_note as note
import partials.buttons.text_button as text_button



def start():

    # Define constants for the screen width and height
    SCREEN_WIDTH = pygame.display.get_surface().get_size()[0]
    SCREEN_HEIGHT = pygame.display.get_surface().get_size()[1]

    PLAY_LINE_LOCATION = 290

    # Variable to keep our main loop running
    running = True
    paused = False






    # Setup for sounds, defaults are good
    pygame.mixer.init()

    # Initialize pygame
    pygame.init()

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()

    



    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_img = pygame.image.load('assets/images/backgrounds/park.jpeg')
    bg_img = pygame.transform.scale(bg_img,(SCREEN_WIDTH,SCREEN_HEIGHT))


    transparent_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - 200), pygame.SRCALPHA)
    transparent_surface.fill((255,255,255, 10))
    pygame.Surface.set_alpha(transparent_surface, 140)

 


   
    # Create our 'player'
    player = playing_player.Player(top_padding=400)



    # Create custom events for adding a Note
    ADDNote = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDNote, 1000)
    

    # Create groups to hold Note sprites, and all sprites
    # - Notes is used for position updates
    # - all_sprites isused for rendering
    Notes = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)



    # Load and play our background music
    pygame.mixer.music.load("assets/sounds/background-music/metro-34-60bpm.mp3")
    pygame.mixer.music.play(loops=-1)
    
    
    # These are the buttons for the pause menu
    resume_button = text_button.TextButton(text="Resume", width= 100,height= 50, left_padding= SCREEN_WIDTH/2 - 50, top_padding= SCREEN_HEIGHT/2 - 50)
    main_menu_button = text_button.TextButton(text="Main Menu", width= 100,height= 50, left_padding= SCREEN_WIDTH/2 - 50, top_padding= SCREEN_HEIGHT/2 +20)
    quit_button = text_button.TextButton(text="Quit", width= 100,height= 50, left_padding= SCREEN_WIDTH/2 - 50, top_padding= SCREEN_HEIGHT/2 + 90)

    # This is the transparent background for the pause menu

    tabs_image = pygame.image.load("assets/images/backgrounds/tabs_outline.png").convert()
    tabs_image.set_colorkey((255, 255, 255), RLEACCEL)

    play_line_image = pygame.image.load("assets/images/backgrounds/play_line.png").convert()
    play_line_image.set_colorkey((255, 255, 255), RLEACCEL)


    # Our main loop
    while running:
        if paused == True:
            # The control loop for when the game is paused
            pygame.mixer.music.pause()
            for event in pygame.event.get():
                # Did the user hit a key?
                if event.type == KEYDOWN:
                    # Was it the Escape key? If so, stop the loop
                    if event.key == K_ESCAPE:
                        # running = False
                        pygame.mixer.music.unpause()
                        paused = False

                # Did the user click the window close button? If so, exit
                elif event.type == QUIT:
                    exit()
            
                # Here we check for hover events 
                if event.type==pygame.MOUSEMOTION:
                    resume_button.on_hover()
                    main_menu_button.on_hover()
                    quit_button.on_hover()
                   
                # Here we check for clicks events 
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if (resume_button.is_pressed() == True):
                        paused = False
                        pygame.mixer.music.unpause()

                    elif(main_menu_button.is_pressed() == True):
                        running = False

                    elif(quit_button.is_pressed() == True):
                        exit()

            # This visually updates the buttons on the pause screen
            screen.blit(resume_button.render, resume_button.button_position)
            screen.blit(main_menu_button.render, main_menu_button.button_position)
            screen.blit(quit_button.render, quit_button.button_position)

            # This is the transparent background for the pause screen
            screen.blit(transparent_surface, (30, 30))

            pygame.display.update()
            
		
    
        else:
            
            # Look at every event in the queue
            for event in pygame.event.get():
                # Did the user hit a key?
                if event.type == KEYDOWN:
                    # Was it the Escape key? If so, pause the loop
                    if event.key == K_ESCAPE:
                        paused = True
                    elif event.key == K_a:
                        print("Pressed A")
                    elif event.key == K_b:
                        print("Pressed B")
                    elif event.key == K_c:
                        print("Pressed C")
                    elif event.key == K_d:
                        print("Pressed D")
                    elif event.key == K_e:
                        print("Pressed E")
                    elif event.key == K_f:
                        print("Pressed F")
                    elif event.key == K_g:
                        print("Pressed G")

                # Did the user click the window close button? If so, exit
                elif event.type == QUIT:
                    exit()


                # Should we add a new Note?
                elif event.type == ADDNote:
                    # Create the new Note, and add it to our sprite groups
                    new_Note1 = note.Note(text="O", tab_line=1, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT)
                    new_Note2 = note.Note(text="O", tab_line=2, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT)
                    new_Note3 = note.Note(text="O", tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT)
                    new_Note4 = note.Note(text="O", tab_line=4, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT)
                    new_Note5 = note.Note(text="O", tab_line=5, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT)
                    new_Note6 = note.Note(text="O", tab_line=6, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT)
                   
                    
                    Notes.add(new_Note1)
                    Notes.add(new_Note2)
                    Notes.add(new_Note3)
                    Notes.add(new_Note4)
                    Notes.add(new_Note5)
                    Notes.add(new_Note6)

                    all_sprites.add(new_Note1)
                    all_sprites.add(new_Note2)
                    all_sprites.add(new_Note3)
                    all_sprites.add(new_Note4)
                    all_sprites.add(new_Note5)
                    all_sprites.add(new_Note6)



            # Get the set of keys pressed and check for user input
            pressed_keys = pygame.key.get_pressed()
            player.update(pressed_keys)




            # Update the position of our Notes
            Notes.update()




            # Fill the screen with the background image
            screen.blit(bg_img,(0,0))
            screen.blit(play_line_image,(0,0))
            screen.blit(tabs_image,(0,0))
            
             
            # Draw all our sprites
            for entity in all_sprites:
                screen.blit(entity.surf, entity.rect)


            # Flip everything to the display
            pygame.display.flip()
            # Ensure we maintain a 30 frames per second rate
            clock.tick(30)




    # At this point, we're done, so we can stop and quit the mixer
    pygame.mixer.music.stop()
    pygame.mixer.quit()