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
    def __init__(self, midi=40, text="O", tab_line=1, time_to_next_note=1.0, font_size=70, font_color=(0, 0, 0), font_name='freesansbold.ttf', Screen_Width=800, Screen_Height=600):
        super(Note, self).__init__()

        # Initialize Pygame
        pygame.init()

        self.was_pressed = False
        self.midi = midi

         # this is a multiplier that is used to figure out how many beats later the next note should come
        # after each note is created this is dynamically updated by calling a function on that note
        # 1.0 means that the next note plays one beat later, 2.0 is 2 beats later while 0.5 would be half a beat later
        self.time_to_next_note = time_to_next_note

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

        # the y value the note should start from
        starting_y = 0

        # the y value the first tab line starts from
        FIRST_HEIGHT = 30

        # how far apart each tab line is 
        TAB_OFFSET = 66

        # This will assign the note a y height based off what tab line it should be on
        if tab_line== 1:
            starting_y = FIRST_HEIGHT
        elif tab_line== 2:
            starting_y = FIRST_HEIGHT + TAB_OFFSET * 1
        elif tab_line== 3:
            starting_y = FIRST_HEIGHT + TAB_OFFSET * 2
        elif tab_line== 4:
            starting_y = FIRST_HEIGHT + TAB_OFFSET * 3
        elif tab_line== 5:
            starting_y = FIRST_HEIGHT + TAB_OFFSET * 4
        elif tab_line== 6:
            starting_y = FIRST_HEIGHT + TAB_OFFSET * 5
            
        # This will start it centered on the right tab line
        self.rect = self.surf.get_rect(
            center=(
                Screen_Width-10, # I added this offset of 10 to make it match up with the metronome time
                starting_y
            )
        )

    # Move the Note based on a constant speed
    # The move number (the -5.666666) was determined with the following :
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
    
    # returns true if the correct key for this button was pressed
    def check_correct_key(self, pressed_key):
        # checks to see if this note has already been pressed
        if self.was_pressed == False:

            # checks if the pressed key matches this note
            if pressed_key == self.keys_dict[self.text]:
                self.was_pressed = True
                return True
            else: 
                return False
    
    def check_correct_note(self, predicted_midi):
        
        if self.was_pressed == False:

            if self.midi == predicted_midi:
                self.was_pressed = True
                return True
            else:
                return False

    # returns the time to the next note
    def get_time_to_next_note(self):
        return self.time_to_next_note