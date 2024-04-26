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
        """
    A class representing the player character.

    Attributes:
        surf (pygame.Surface): The player character's surface.
        rect (pygame.Rect): The player character's rectangular area.
        screen_height (int): The height of the game screen.
        screen_width (int): The width of the game screen.

    Methods:
        __init__(self, asset_path="assets/images/characters/player/protaganist.png",
            screen_height=800, screen_width=600, top_padding=340):
            Initializes the Player object with the provided parameters.
        
        update(self, pressed_keys):
            Updates the player's position based on the pressed keys and keeps the player on the screen.
    """
        def __init__(self, asset_path="assets/images/characters/player/protaganist.png", screen_height=800, screen_width=600, top_padding=340):
            """
        Initializes the Player object with the provided parameters.

        Args:
            asset_path (str): The file path of the player character's image asset.
            screen_height (int): The height of the game screen.
            screen_width (int): The width of the game screen.
            top_padding (int): The vertical offset to position the player character at the top of the screen.
        """
            super(Player, self).__init__()
            self.surf = pygame.image.load(asset_path).convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.rect = self.surf.get_rect()
            self.screen_height = screen_height
            self.screen_width = screen_width

            #sets the top at an offset of 340 to get him to look like he's standing on the ground
            self.rect.top = top_padding

        # Move the sprite based on keypresses
        def update(self, pressed_keys):
            """
        Updates the player's position based on the pressed keys and keeps the player on the screen.

        Args:
            pressed_keys (dict): A dictionary representing the state of keyboard keys, where
                the keys are pygame key constants and the values are Boolean values indicating
                whether the corresponding key is pressed.
        """
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

            # Keep player on the screen
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > self.screen_width:
                self.rect.right = self.screen_width
            if self.rect.top <= 0:
                self.rect.top = 0
            elif self.rect.bottom >= self.screen_height:
                self.rect.bottom = self.screen_height