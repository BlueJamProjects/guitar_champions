# Import the pygame module
import pygame

# Import random for random numbers
import random


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

def start():

    # Define constants for the screen width and height
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600


    # Define the Player object extending pygame.sprite.Sprite
    # Instead of a surface, we use an image for a better looking sprite
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.surf = pygame.image.load("assets/images/characters/protaganist.png").convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.rect = self.surf.get_rect()

            #sets the top at an offset of 340 to get him to look like he's standing on the ground
            self.rect.top = 340

        # Move the sprite based on keypresses
        def update(self, pressed_keys):
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

            # Keep player on the screen
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.rect.top <= 0:
                self.rect.top = 0
            elif self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT


    class Note(pygame.sprite.Sprite):
        def __init__(self):
            super(Note, self).__init__()

            self.surf = pygame.image.load("assets/images/notes/C.png").convert()

            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            # The starting position is randomly generated
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT-200),
                )
            )

        # Move the Note based on a constant speed
        # Remove it when it passes the left edge of the screen
        def update(self):
            self.rect.move_ip(-5, 0)
            if self.rect.right < 0:
                self.kill()


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
    # Create custom events for adding a Note
    ADDNote = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDNote, 2500)
    # Create our 'player'
    player = Player()
    # Create groups to hold Note sprites, and all sprites
    # - Notes is used for position updates
    # - all_sprites isused for rendering
    Notes = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    # Load and play our background music
    pygame.mixer.music.load("assets/sounds/background-music/smoke-on-water.mp3")
    pygame.mixer.music.play(loops=-1)
    # Variable to keep our main loop running
    running = True
    # Our main loop
    while running:
        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop
                if event.key == K_ESCAPE:
                    running = False
            # Did the user click the window close button? If so, stop the loop
            elif event.type == QUIT:
                running = False
            # Should we add a new Note?
            elif event.type == ADDNote:
                # Create the new Note, and add it to our sprite groups
                new_Note = Note()
                Notes.add(new_Note)
                all_sprites.add(new_Note)
        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        # Update the position of our enemies and Notes
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