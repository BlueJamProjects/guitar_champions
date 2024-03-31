# Import the pygame module
import pygame



class TutorialPopup():
        
        def __init__(self,
                      text, 
                      width=300, 
                      height=200, 
                      left_padding = 100, 
                      top_padding=50, 
                      button_color=(239,159,20), 
                      button_hover_color=(209,129,0), 
                      text_color=(255, 255, 255),
                      background_color=(0,0,0)
                      ):
            super(TutorialPopup, self).__init__()

            
            
           
        
            
 
            # creates the outline box render elements
            self.outline_color = background_color
            self.outline_position = pygame.Rect(left_padding - 10, top_padding - 10, width, height + 20)



             # The text on the pop up
            self.body_text = text
            self.background_color = background_color
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
                    elif current_string_length + len(word) <= 44:
                        line1_text = line1_text + " " + word
                        current_string_length = current_string_length + len(word) + 1
                    else:
                        line2_text = word
                        current_string_length = len(word)
                        current_line = 2

                elif current_line == 2:
                   if current_string_length + len(word) <= 44:
                       line2_text = line2_text + " " + word
                       current_string_length = current_string_length + len(word) + 1
                   else:
                       line3_text = word
                       current_string_length = len(word)
                       current_line = 3
                
                elif current_line == 3:
                   if current_string_length+ len(word) <= 44:
                       line3_text = line3_text + " " + word
                       current_string_length = current_string_length + len(word) + 1
                   else:
                       line4_text = word
                       current_string_length = len(word)
                       current_line = 4

                elif current_line == 4:
                   if current_string_length+ len(word) <= 44:
                       line4_text = line4_text + " " + word
                       current_string_length = current_string_length + len(word) + 1
                   else:
                       line5_text = word
                       current_string_length = len(word)
                       current_line = 5
                
                else:
                    line5_text = line5_text + " " + word




            self.line1_font = pygame.font.Font("assets/font/arial.ttf",14)
            self.line1_position = pygame.Rect(left_padding, top_padding, width, height)
            self.line1_render = self.line1_font.render(line1_text, True, self.text_color, self.background_color)


            self.line2_font = pygame.font.Font("assets/font/arial.ttf",14)
            self.line2_position = pygame.Rect(left_padding, top_padding+ 30, width, height)
            self.line2_render = self.line2_font.render(line2_text, True, self.text_color, self.background_color)

            self.line3_font = pygame.font.Font("assets/font/arial.ttf",14)
            self.line3_position = pygame.Rect(left_padding, top_padding+ 60, width, height)
            self.line3_render = self.line3_font.render(line3_text, True, self.text_color, self.background_color)

            self.line4_font = pygame.font.Font("assets/font/arial.ttf",14)
            self.line4_position = pygame.Rect(left_padding, top_padding+ 90, width, height)
            self.line4_render = self.line4_font.render(line4_text, True, self.text_color, self.background_color)

            self.line5_font = pygame.font.Font("assets/font/arial.ttf",14)
            self.line5_position = pygame.Rect(left_padding, top_padding+ 120, width, height)
            self.line5_render = self.line4_font.render(line5_text, True, self.text_color, self.background_color)

            
            self.number_font = pygame.font.Font("assets/font/arial.ttf", 14)
            self.number_position = pygame.Rect(left_padding + width - 50, top_padding + height - 10, width, height)
            self.number_render = self.number_font.render("1/2", True, self.text_color, self.background_color)



            # Creates the button render elements

            self.button_text_color = text_color
            self.button_current_color = button_color
            self.button_color = button_color
            self.button_hover_color = button_hover_color
            self.button_text = "Next"


            self.button_font = pygame.font.Font("assets/font/Signatra.ttf",40)
            self.button_position = pygame.Rect(left_padding+ width/2 - 30, top_padding+height-40, width, height)
            self.button_render = self.button_font.render(self.button_text, True, self.button_text_color, self.button_color)




        def set_number(self, current_number, total):
            self.number_render = self.number_font.render(str(current_number) + "/" + str(total), True, self.text_color, self.background_color)




        def button_on_hover(self):
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
            # This function checks whether the button is being pressed and returns True if so
            # This should be placed in the control loop after if event.type==pygame.MOUSEBUTTONDOWN:

            mouse_position=pygame.mouse.get_pos()
            if self.button_position.collidepoint(mouse_position):
                # print("Pressed")
                return True
            else:
                # print("Not pressed")
                return False 