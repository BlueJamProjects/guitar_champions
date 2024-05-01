# Import the pygame module
import pygame

"""
This file contains the TitleCard class
"""



class Titlecard():
        """
    A class representing a title card for our application.

    Attributes:
        text (str): The text to be displayed on the title card.
        width (int): The width of the title card (default is 100).
        height (int): The height of the title card (default is 70).
        left_padding (int): The left padding of the title card (default is 100).
        top_padding (int): The top padding of the title card (default is 50).
        color (tuple): The RGB color tuple representing the background color of the title card (default is (255, 187, 68)).
        text_color (tuple): The RGB color tuple representing the color of the text on the title card (default is (0, 0, 0)).

    Methods:
        __init__: Initializes a Titlecard object with the specified attributes.
    """
        
        def __init__(self,
                      text, 
                      width=100, 
                      height=70, 
                      left_padding = 100, 
                      top_padding=50, 
                      color=(255,187,68), 
                      text_color=(0,0,0)):
            super(Titlecard, self).__init__()
            self.button_position = pygame.Rect(left_padding, top_padding, width, height)
            self.color = color
            self.text_color = text_color
            self.current_color = color
            self.text = text
        
            # create a font to select font and size
            self.font = pygame.font.Font("assets/font/ka1.ttf",50)
          
            # create a text surface object using the font
            # on which text is drawn on it.
            self.render = self.font.render(self.text, True, self.text_color, self.color)

