"""
This file contains the laternate Note class
"""

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
        """
    A class representing musical notes in a game.

    Attributes:
        surf (pygame.Surface): The image surface of the note.
        rect (pygame.Rect): The rectangular area representing the note's position and size.

    Args:
        asset_path (str): The file path to the image of the note (default: "assets/images/notes/C.png").
        Screen_Width (int): The width of the game screen (default: 800).
        Screen_Height (int): The height of the game screen (default: 600).

    Note:
        The note's starting position is randomly generated within the screen boundaries.
        """

        def __init__(self, asset_path="assets/images/notes/C.png", Screen_Width =800, Screen_Height=600):
            """
        Initializes a Note object.

        Args:
            asset_path (str): The file path to the image of the note.
            Screen_Width (int): The width of the game screen.
            Screen_Height (int): The height of the game screen.
            """
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
            """
            Moves the note based on a constant speed and removes it when it passes the left edge of the screen.
            """
            self.rect.move_ip(-5, 0)
            if self.rect.right < 0:
                self.kill()
