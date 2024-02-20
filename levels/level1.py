# Import the pygame module
import pygame

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
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

import partials.player.jason_main as jason_main
import partials.notes.c_note as c_note

def start():

    # Define constants for the screen width and height
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600


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
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    bg_img = pygame.image.load('assets/images/backgrounds/mario level.png')
    bg_img = pygame.transform.scale(bg_img,(SCREEN_WIDTH,SCREEN_HEIGHT))






   
    # Create our 'player'
    player = jason_main.Player()



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
    

    # left padding, top padding, width, height
    button_position=pygame.Rect(SCREEN_WIDTH/2 - SCREEN_HEIGHT/8,SCREEN_HEIGHT/2,SCREEN_HEIGHT/4,SCREEN_HEIGHT/16)
    cornflower_blue=(128,149,255)
    button_color=cornflower_blue

    



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

                mouse_position=pygame.mouse.get_pos()

                if event.type==pygame.MOUSEMOTION:
                    if button_position.collidepoint(mouse_position):
                      print("Hover")
                    else:
                        print("Other hover")

                if event.type==pygame.MOUSEBUTTONDOWN:
                    if button_position.collidepoint(mouse_position):
                        print("Clicked")
            pygame.draw.rect(screen,(button_color),(button_position))
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
                    exit()


                # Should we add a new Note?
                elif event.type == ADDNote:
                    # Create the new Note, and add it to our sprite groups
                    new_Note = c_note.Note(Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT)
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