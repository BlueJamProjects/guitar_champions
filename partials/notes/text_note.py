import pygame
import random

from pygame.locals import (
    K_o,
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
)

class Note(pygame.sprite.Sprite):
    def __init__(self, text="O", tab_line=1, font_size=70, font_color=(0, 0, 0), font_name='freesansbold.ttf', Screen_Width=800, Screen_Height=600):
        super(Note, self).__init__()

        # Initialize Pygame
        pygame.init()

        # Set up font 
        self.font = pygame.font.SysFont(font_name, font_size)
        self.text = text
        self.font_color = font_color

        # Render text onto the surface
        self.surf = self.font.render(self.text, True, self.font_color)


        # This dictionary matches notes to keys pressed
        self.keys_dict = {
        "O": K_o,
        "10": K_0,
        "1": K_1,
        "2": K_2,
        "3": K_3,
        "4": K_4,
        "5": K_5,
        "6": K_6,
        "7": K_7,
        "8": K_8,
        "9": K_9,

        }


        starting_y = 0

        FIRST_HEIGHT = 30
        NOTE_OFFSET = 66

        # This will assign the note a y height based off what tab line it should be on
        if tab_line== 1:
            starting_y = FIRST_HEIGHT
        elif tab_line== 2:
            starting_y = FIRST_HEIGHT + NOTE_OFFSET * 1
        elif tab_line== 3:
            starting_y = FIRST_HEIGHT + NOTE_OFFSET * 2
        elif tab_line== 4:
            starting_y = FIRST_HEIGHT + NOTE_OFFSET * 3
        elif tab_line== 5:
            starting_y = FIRST_HEIGHT + NOTE_OFFSET * 4
        elif tab_line== 6:
            starting_y = FIRST_HEIGHT + NOTE_OFFSET * 5
            
        # This will start it centered on the right tab line
        self.rect = self.surf.get_rect(
            center=(
                Screen_Width-10, # I added this offset of 10 to make it match up with the metronome time
                starting_y
                
            )
        )

    # Move the Note based on a constant speed
    # The move number was determined with the following :
        # Screen distance to the play line / 90 frames
        # the 90 frames are so that it takes 3 seconds
        # the 3 seconds were chosen as the song will start on the 4th metronome beat
        # this gives the player time to get ready
        # IMPORTANT if you change these numbers please update this comment

    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5.666666, 0)
        if self.rect.right < 0:
            self.kill()


    # This returns the current x location of the note
    def get_x_location(self):
        return self.rect.right
    
    def check_correct_key(self, pressed_key):
        if pressed_key == self.keys_dict[self.text]:
            return True
        else: 
            return False