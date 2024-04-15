# Import the pygame module
import pygame


# Import random for random numbers
import random

import sys

import os


# Import the menu library to more easily make menu selction
import pygame_menu

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    RLEACCEL,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
# width=pygame.display.get_surface().get_size()[1]/4, height=pygame.display.get_surface().get_size()[1]/16, left_padding = pygame.display.get_surface().get_size()[0]/2 - pygame.display.get_surface().get_size()[1]/8, top_padding=pygame.display.get_surface().get_size()[1]/2
import partials.player.movable_player as movable_player
import partials.notes.note as note
import partials.buttons.text_button as text_button



def start():

    # Define constants for the screen width and height
    SCREEN_WIDTH = pygame.display.get_surface().get_size()[0]
    SCREEN_HEIGHT = pygame.display.get_surface().get_size()[1]


    # Variable to keep our main loop running
    running = True
    paused = False






    # Setup for sounds, defaults are good
    pygame.mixer.init()

    # Initialize pygame
    pygame.init()

    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()

    



    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_img = pygame.image.load('assets/images/backgrounds/greenmountains.png')
    bg_img = pygame.transform.scale(bg_img,(SCREEN_WIDTH,SCREEN_HEIGHT))






   
    # Create our 'player'
    player = movable_player.Player()



    # Create custom events for adding a Note
    ADDNote = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDNote, 2500)
    

    # Create groups to hold Note sprites, and all sprites
    # - Notes is used for position updates
    # - all_sprites isused for rendering
    Notes = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)



    # Load and play our background music
    pygame.mixer.music.load("assets/sounds/background-music/smoke-on-water.mp3")
    pygame.mixer.music.play(loops=-1)
    
    
    # These are the buttons for the pause menu
    resume_button = text_button.TextButton(text="Resume", width= 100,height= 50, left_padding= SCREEN_WIDTH/2 - 50, top_padding= SCREEN_HEIGHT/2 - 50)
    main_menu_button = text_button.TextButton(text="Main Menu", width= 100,height= 50, left_padding= SCREEN_WIDTH/2 - 50, top_padding= SCREEN_HEIGHT/2 +20)
    quit_button = text_button.TextButton(text="Quit", width= 100,height= 50, left_padding= SCREEN_WIDTH/2 - 50, top_padding= SCREEN_HEIGHT/2 + 90)

    # This is the transparent background for the pause menu
    transparent_surface = pygame.Surface((SCREEN_WIDTH - 60, SCREEN_HEIGHT - 60), pygame.SRCALPHA)
    transparent_surface.fill((255,187,68, 10))
    pygame.Surface.set_alpha(transparent_surface, 140)

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
                    os._exit(status=0)
            
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
                        restart_level = False
                        running = False

                    elif(quit_button.is_pressed() == True):
                        os._exit(status=0)

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

                # Did the user click the window close button? If so, exit
                elif event.type == QUIT:
                    os._exit(status=0)


                # Should we add a new Note?
                elif event.type == ADDNote:
                    # Create the new Note, and add it to our sprite groups
                    new_Note = note.Note(asset_path="assets/images/notes/C.png",Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT)
                    Notes.add(new_Note)
                    all_sprites.add(new_Note)



            # Get the set of keys pressed and check for user input
            pressed_keys = pygame.key.get_pressed()
            player.update(pressed_keys)




            # Update the position of our Notes
            Notes.update()




            # Fill the screen with the background image
            screen.blit(bg_img,(0,0))
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