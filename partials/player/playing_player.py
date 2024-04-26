import pygame
from pygame.locals import (
    RLEACCEL,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)



class Player(pygame.sprite.Sprite):
        """A class representing the player character in the game.

    Args:
        asset_path (str): The path to the image asset for the player character. Default is "assets/images/characters/player/protaganist.png".
        screen_height (int): The height of the game screen. Default is 800 pixels.
        screen_width (int): The width of the game screen. Default is 600 pixels.
        top_padding (int): The offset from the top of the screen to position the player character. Default is 340 pixels.

    Attributes:
        surf (pygame.Surface): The surface representing the player character.
        rect (pygame.Rect): The rectangular area occupied by the player character.
        screen_height (int): The height of the game screen.
        screen_width (int): The width of the game screen.

    Note:
        The player character is initially positioned at the left side of the screen with an offset to appear on the ground.
    """
        def __init__(self, asset_path="assets/images/characters/player/protaganist.png", screen_height=800, screen_width=600, top_padding=340):
            super(Player, self).__init__()
            self.surf = pygame.image.load(asset_path).convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.rect = self.surf.get_rect()
            self.screen_height = screen_height
            self.screen_width = screen_width

            #sets the top at an offset of 340 to get him to look like he's standing on the ground
            self.rect.top = top_padding
            self.rect.left = 30

        # Move the sprite based on keypresses
        def update(self, pressed_keys):
            """Update the position of the player character based on keypresses.

        Args:
            pressed_keys (dict): A dictionary representing the keys currently pressed.

        Note:
            The player character moves horizontally based on the arrow keys.
        """
            pass
