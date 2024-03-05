# Import the pygame module
import pygame

# Import random for random numbers
import random

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

class Note(pygame.sprite.Sprite):
        def __init__(self, asset_path="assets/images/notes/C.png", Screen_Width =800, Screen_Height=600):
            super(Note, self).__init__()

            self.surf = pygame.image.load(asset_path).convert()

            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            # The starting position is randomly generated
            self.rect = self.surf.get_rect(
                center=(
                    random.randint( Screen_Width + 20,  Screen_Width + 100),
                    random.randint(0, Screen_Height-200),
                )
            )

        # Move the Note based on a constant speed
        # Remove it when it passes the left edge of the screen
        def update(self):
            self.rect.move_ip(-5, 0)
            if self.rect.right < 0:
                self.kill()
