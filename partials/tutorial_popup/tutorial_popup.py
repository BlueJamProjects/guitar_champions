# Import the pygame module
import pygame

"""
This file contains the TutorialPopup class
"""



class TutorialPopup():
        """
    A class representing our tutorial popup window in our Pygame application.

    Attributes:
        text (str): The text content of the popup.
        width (int): The width of the popup window. Defaults to 290.
        height (int): The height of the popup window. Defaults to 200.
        left_padding (int): The left padding of the popup window. Defaults to 100.
        top_padding (int): The top padding of the popup window. Defaults to 50.
        button_color (tuple): The color of the popup button. Defaults to (239, 159, 20).
        button_hover_color (tuple): The hover color of the popup button. Defaults to (209, 129, 0).
        text_color (tuple): The color of the text in the popup. Defaults to (255, 255, 255).
        background_color (tuple): The background color of the popup. Defaults to (239, 159, 20).
        show_highlight_region (bool): Whether to show a highlighted region. Defaults to False.
        highlight_region_color (tuple): The color of the highlighted region. Defaults to (255, 255, 255).
        highlight_region_position (pygame.Rect): The position of the highlighted region. Defaults to pygame.Rect(20, 20, 100, 100).
        trigger_effect_number (int): A number used to trigger effects. Defaults to 0.
        is_final_popup (bool): Indicates if this is the final popup. Defaults to False.
    """
        
        def __init__(self,
                      text, 
                      width=290, 
                      height=200, 
                      left_padding = 100, 
                      top_padding=50, 
                      button_color=(239,159,20), 
                      button_hover_color=(209,129,0), 
                      text_color=(255, 255, 255),
                      background_color=(239,159,20),
                      show_hightlight_region=False,
                      highlight_region_color=(255, 255, 255),
                      highlight_region_position = pygame.Rect(20, 20, 100, 100),
                      trigger_effect_number=0,
                      is_final_popup=False,

                      ):
            super(TutorialPopup, self).__init__()


            # IMPORTANT
            # You should not change width and height to get the popup to display properly with the text


            # this is True if this is a final popup
            self.is_final_popup = is_final_popup
            
            # This is a number can be checked in the tutorial to see if an effect should be triggered when this button is moved away from
            self.trigger_effect_number = trigger_effect_number

        

            # creates the outline box (The box that surrounds the text) render elements
            self.outline_color = background_color
            self.outline_position = pygame.Rect(left_padding - 10, top_padding - 10, width, height + 20)



             # The text on the pop up
            self.body_text = text

            # The background color of the text
            self.background_color = background_color

            # the color of the text
            self.text_color = text_color

            line1_text = ""
            line2_text = ""
            line3_text = ""
            line4_text = ""
            line5_text = ""
            

            

            # The below code splits the text into a list of words
            # Then it iterates through the words to build up each line
            # Finally any excess words will go to the 5th line
            text_words_list = text.split(" ")

            current_string_length = 0

            current_line = 1

            for word in text_words_list:
                if current_line == 1:
                    if current_string_length == 0:
                        line1_text = word
                        current_string_length = len(word)
                    elif current_string_length + len(word) <= 42:
                        line1_text = line1_text + " " + word
                        current_string_length = current_string_length + len(word) + 1
                    else:
                        line2_text = word
                        current_string_length = len(word)
                        current_line = 2

                elif current_line == 2:
                   if current_string_length + len(word) <= 42:
                       line2_text = line2_text + " " + word
                       current_string_length = current_string_length + len(word) + 1
                   else:
                       line3_text = word
                       current_string_length = len(word)
                       current_line = 3
                
                elif current_line == 3:
                   if current_string_length+ len(word) <= 42:
                       line3_text = line3_text + " " + word
                       current_string_length = current_string_length + len(word) + 1
                   else:
                       line4_text = word
                       current_string_length = len(word)
                       current_line = 4

                elif current_line == 4:
                   if current_string_length+ len(word) <= 42:
                       line4_text = line4_text + " " + word
                       current_string_length = current_string_length + len(word) + 1
                   else:
                       line5_text = word
                       current_string_length = len(word)
                       current_line = 5
                
                else:
                    line5_text = line5_text + " " + word




            self.line1_font = pygame.font.Font("assets/font/arial-unicode-bold.ttf",13)
            self.line1_position = pygame.Rect(left_padding, top_padding, width, height)
            self.line1_render = self.line1_font.render(line1_text, True, self.text_color)


            self.line2_font = pygame.font.Font("assets/font/arial-unicode-bold.ttf",13)
            self.line2_position = pygame.Rect(left_padding, top_padding+ 30, width, height)
            self.line2_render = self.line2_font.render(line2_text, True, self.text_color)

            self.line3_font = pygame.font.Font("assets/font/arial-unicode-bold.ttf",13)
            self.line3_position = pygame.Rect(left_padding, top_padding+ 60, width, height)
            self.line3_render = self.line3_font.render(line3_text, True, self.text_color)

            self.line4_font = pygame.font.Font("assets/font/arial-unicode-bold.ttf",13)
            self.line4_position = pygame.Rect(left_padding, top_padding+ 90, width, height)
            self.line4_render = self.line4_font.render(line4_text, True, self.text_color)

            self.line5_font = pygame.font.Font("assets/font/arial-unicode-bold.ttf",13)
            self.line5_position = pygame.Rect(left_padding, top_padding+ 120, width, height)
            self.line5_render = self.line4_font.render(line5_text, True, self.text_color)

            
            self.number_font = pygame.font.Font("assets/font/arial.ttf", 14)
            self.number_position = pygame.Rect(left_padding + width - 50, top_padding + height - 10, width, height)
            self.number_render = self.number_font.render("1/2", True, self.text_color)

            self.show_hightlight_region = show_hightlight_region
            self.highlight_region_color = highlight_region_color
            self.highlight_region_position = highlight_region_position


            # sets the button properties

            self.button_text_color = text_color
            self.button_current_color = button_color
            self.button_color = button_color
            self.button_hover_color = button_hover_color

            self.button_text = " Next"


            # Creates the button render elements
            self.button_font = pygame.font.Font("assets/font/Signatra.ttf",40)
            self.button_position = pygame.Rect(left_padding+ width/2 - 42, top_padding+height-40, 62, 44)

            if self.is_final_popup == True:
                self.button_text = "Complete"
                self.button_position = pygame.Rect(left_padding+ width/2 - 62, top_padding+height-40, 105, 44)


            self.button_render = self.button_font.render(self.button_text, True, self.button_text_color, (209,129,0))




        def set_number(self, current_number, total):
            """
        Creates the render for the current popups number.

        Args:
            current_number (int): The current number to render.
            total (int): The total number to render.

        Returns:
            None
        """
            self.number_render = self.number_font.render(str(current_number) + "/" + str(total), True, self.text_color, self.background_color)




        def button_on_hover(self):
            """Check whether the button is being hovered over and changes style accordingly.

        This method should be placed in the control loop after if event.type == pygame.MOUSEMOTION.

        Returns:
            None
        """
            # This funciton checks whether the button is being hovered over and changes style accordingly
            # This should be placed in the control loop after if event.type==pygame.MOUSEMOTION:

            mouse_position=pygame.mouse.get_pos()
            if self.button_position.collidepoint(mouse_position):
                # print("Hovering")
                self.button_current_color = self.button_hover_color
                        
            else:
                # print("Not hovering")
                self.button_current_color = self.button_color

            self.render = self.button_font.render(self.button_text, True, self.button_text_color, self.button_current_color)


        def button_is_pressed(self):
            """Checks whether the button is being pressed.

        Returns:
            bool: True if the button is pressed, False otherwise.
        """
            
            # This function checks whether the button is being pressed and returns True if so
            # This should be placed in the control loop after if event.type==pygame.MOUSEBUTTONDOWN:

            mouse_position=pygame.mouse.get_pos()
            if self.button_position.collidepoint(mouse_position):
                # print("Pressed")
                return True
            else:
                # print("Not pressed")
                return False 