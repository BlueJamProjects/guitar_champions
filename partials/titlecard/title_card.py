# Import the pygame module
import pygame



class Titlecard():
        
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

