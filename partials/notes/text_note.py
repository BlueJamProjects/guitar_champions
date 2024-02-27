import pygame
import random

class Note(pygame.sprite.Sprite):
    def __init__(self, text="C", font_size=70, font_color=(0, 0, 0), font_name='freesansbold.ttf', Screen_Width=800, Screen_Height=600):
        super(Note, self).__init__()

        # Initialize Pygame
        pygame.init()

        # Set up font
        self.font = pygame.font.SysFont(font_name, font_size)
        self.text = text
        self.font_color = font_color

        # Render text onto the surface
        self.surf = self.font.render(self.text, True, self.font_color)


        starting_y = 0

        A_HEIGHT = 10
        NOTE_OFFSET = 20

        if text == "A":
            starting_y = A_HEIGHT
        elif text == "B":
            starting_y = A_HEIGHT + NOTE_OFFSET * 1
        elif text == "C":
            starting_y = A_HEIGHT + NOTE_OFFSET * 2
        elif text == "D":
            starting_y = A_HEIGHT + NOTE_OFFSET * 3
        elif text == "E":
            starting_y = A_HEIGHT + NOTE_OFFSET * 4
        elif text == "F":
            starting_y = A_HEIGHT + NOTE_OFFSET * 5
        elif text == "G":
            starting_y = A_HEIGHT + NOTE_OFFSET * 6

        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                Screen_Width + 20,
                starting_y
                # random.randint(0, Screen_Height - 500),
                
            )
        )

    # Move the Note based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
