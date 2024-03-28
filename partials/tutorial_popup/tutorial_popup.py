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

            gap_1 = text.find(" ", 40, 50)

            line1_text = text[0: gap_1 :1]

            self.line1_font = pygame.font.Font("assets/font/Signatra.ttf",22)
            self.line1_position = pygame.Rect(left_padding, top_padding, width, height)
            self.line1_render = self.line1_font.render(line1_text, True, self.text_color, self.background_color)

            gap_2 = text.find(" ", gap_1+40, gap_1+50)

            line2_text = text[gap_1: gap_2 :1]


            self.line2_font = pygame.font.Font("assets/font/Signatra.ttf",22)
            self.line2_position = pygame.Rect(left_padding, top_padding+ 40, width, height)
            self.line2_render = self.line2_font.render(line2_text, True, self.text_color, self.background_color)

            gap_2 = text.find(" ", gap_1+40, gap_1+50)

            line2_text = text[gap_1: gap_2 :1]

            self.line3_font = pygame.font.Font("assets/font/Signatra.ttf",22)
            self.line3_position = pygame.Rect(left_padding, top_padding+ 80, width, height)
            self.line3_render = self.line3_font.render(self.body_text, True, self.text_color, self.background_color)

            self.line4_font = pygame.font.Font("assets/font/Signatra.ttf",22)
            self.line4_position = pygame.Rect(left_padding, top_padding+ 120, width, height)
            self.line4_render = self.line4_font.render(self.body_text, True, self.text_color, self.background_color)

            



            # Creates the button render elements

            self.button_text_color = text_color
            self.button_current_color = button_color
            self.button_color = button_color
            self.button_hover_color = button_hover_color
            self.button_text = "Next"


            self.button_font = pygame.font.Font("assets/font/Signatra.ttf",40)
            self.button_position = pygame.Rect(left_padding+ width/2 - 30, top_padding+height-40, width, height)
            self.button_render = self.button_font.render(self.button_text, True, self.button_text_color, self.button_color)








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