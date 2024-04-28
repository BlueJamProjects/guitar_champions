"""
This file contains the TextButton class
"""


# Import the pygame module
import pygame



class TextButton():
        """A class representing a simple text button in a pygame application.

    Attributes:
        text (str): The text displayed on the button.
        width (int): The width of the button (default is 100).
        height (int): The height of the button (default is 50).
        left_padding (int): The left padding of the button (default is 100).
        top_padding (int): The top padding of the button (default is 50).
        color (tuple): The color of the button in RGB format (default is (239, 159, 20)).
        hover_color (tuple): The color of the button when hovered over (default is (209, 129, 0)).
        text_color (tuple): The color of the text on the button in RGB format (default is (255, 255, 255)).
        button_position (pygame.Rect): The position and dimensions of the button as a pygame Rect object.
        current_color (tuple): The current color of the button.
        font (pygame.font.Font): The font used for the button text.
        render (pygame.Surface): The rendered text surface of the button.
    
    Methods:
        on_hover: Changes the button style when hovered over.
        is_pressed: Checks if the button is being pressed.
        """
        
        def __init__(self,
                      text, 
                      width=100, 
                      height=50, 
                      left_padding = 100, 
                      top_padding=50, 
                      color=(239,159,20), 
                      hover_color=(209,129,0), 
                      text_color=(255, 255, 255)):
            super(TextButton, self).__init__()
            self.button_position = pygame.Rect(left_padding, top_padding, width, height)
            self.color = color
            self.hover_color = hover_color
            self.text_color = text_color
            self.current_color = color
            self.text = text
        
            # create a font to select font and size
            self.font = pygame.font.Font("assets/font/Signatra.ttf",40)
 
            # create a text surface object using the font
            # on which text is drawn on it.
            self.render = self.font.render(self.text, True, self.text_color, self.color)


        def on_hover(self):
            # This funciton checks whether the button is being hovered over and changes style accordingly
            # This should be placed in the control loop after if event.type==pygame.MOUSEMOTION:
            """Changes the style of the button when hovered over.

            This function is intended to be called within the control loop after checking if the event type is pygame.MOUSEMOTION.

            Parameters:
                self: The button object.

            Returns:
                None

            Notes:
                This function updates the button's color based on whether the mouse cursor is hovering over it or not.

            """

            mouse_position=pygame.mouse.get_pos()
            if self.button_position.collidepoint(mouse_position):
                # print("Hovering")
                self.current_color = self.hover_color
                        
            else:
                # print("Not hovering")
                self.current_color = self.color

            self.render = self.font.render(self.text, True, self.text_color, self.current_color)


        def is_pressed(self):
            """
            Checks whether the button is being pressed.
        
            Args:
                self: The Button object.
        
            Returns:
                bool: True if the button is pressed, False otherwise.
        
            Note:
                This function should be placed in the control loop after checking if event.type == pygame.MOUSEBUTTONDOWN.
            """
            # This funciton checks whether the button is being pressed and returns True if so
            # This should be placed in the control loop after if event.type==pygame.MOUSEBUTTONDOWN:

            mouse_position=pygame.mouse.get_pos()
            if self.button_position.collidepoint(mouse_position):
                # print("Pressed")
                return True
            else:
                # print("Not pressed")
                return False 