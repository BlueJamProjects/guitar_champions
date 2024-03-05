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
        def __init__(self, asset_path="assets/images/characters/player/protaganist.png", screen_height=800, screen_width=600, top_padding=340):
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
            pass
            # if pressed_keys[K_g]:
            #     self.rect.move_ip(-5, 0)
            # if pressed_keys[K_RIGHT]:
            #     self.rect.move_ip(5, 0)