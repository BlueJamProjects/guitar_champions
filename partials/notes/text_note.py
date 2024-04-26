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
    def __init__(self, midi=40, text="O", tab_line=1, time_to_next_note=1.0, font_size=70, font_color=(0, 0, 0), font_name='freesansbold.ttf', Screen_Width=800, Screen_Height=600, id=0):
        super(Note, self).__init__()

        # Initialize Pygame
        pygame.init()

        self.tab_line = tab_line

        self.Screen_Width = Screen_Width
        self.Screen_Height = Screen_Height

        self.id=id

        self.midi = midi

        self.was_played = False


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

        self.is_active = False


        # the y value the note should start from
        starting_y = 0

        # the y value the first tab line starts from
        FIRST_HEIGHT = 30

        # how far apart each tab line is 
        # Each line has specific OFFSET since we change the tabs_outline
        TAB_OFFSET = 60

        # This will assign the note a y height based off what tab line it should be on
        if tab_line== 1:
            starting_y = FIRST_HEIGHT - 1
        elif tab_line== 2:
            starting_y = FIRST_HEIGHT + 60 * 1
        elif tab_line== 3:
            starting_y = FIRST_HEIGHT + 61 * 2
        elif tab_line== 4:
            starting_y = FIRST_HEIGHT + 61 * 3
        elif tab_line== 5:
            starting_y = FIRST_HEIGHT + 62 * 4
        elif tab_line== 6:
            starting_y = FIRST_HEIGHT + 63 * 5
            
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
    
    # This sets the current x location of the note
    def set_x_location(self, x_value=100):
        self.rect.right = x_value
    

    
    def check_correct_note(self, predicted_midi_arr):
        
        if self.was_played == False:

            for note in predicted_midi_arr:
                if self.midi == note:
                    self.was_played = True
                    return True
            
            return False

    # returns the time to the next note
    def get_time_to_next_note(self):
        return self.time_to_next_note
    

    # sets the note to be active 
    def set_active_color(self):
        self.is_active = True
        self.font_color = (0,0,255)
        self.surf = self.font.render(self.text, True, self.font_color)


    # returns true if the if the note is active and false otherwise  
    def get_is_active(self):
        return  self.is_active
    

    # sets the color to show that the user didn't hit the right note
    def set_missed_color(self):
        self.font_color = (255,0,0)
        self.surf = self.font.render(self.text, True, self.font_color)

    # sets the color to show that the user did hit the right note
    def set_played_color(self):
        self.font_color = (0,255,0)
        self.surf = self.font.render(self.text, True, self.font_color)

    def get_was_played(self):
        return self.was_played