# Import the pygame module
import pygame



class TutorialPopup():
        
        def __init__(self,
                      text, 
                      width=100, 
                      height=50, 
                      left_padding = 100, 
                      top_padding=50, 
                      color=(239,159,20), 
                      hover_color=(209,129,0), 
                      text_color=(255, 255, 255)):
            super(TutorialPopup, self).__init__()
            
            self.color = color
            self.hover_color = hover_color
            self.text_color = text_color
            self.current_color = color
            self.button_text = "Next"
        
            # create a font to select font and size
            self.font = pygame.font.Font("assets/font/Signatra.ttf",40)
 
            # create a text surface object using the font
            # on which text is drawn on it.
            self.outline_color = (0,0,0)

            self.outline_position = pygame.Rect(left_padding - 10, top_padding - 10, width, height + 20)

            self.button_position = pygame.Rect(left_padding, top_padding, width, height)
            self.render = self.font.render(self.button_text, True, self.text_color, self.color)


        def button_on_hover(self):
            # This funciton checks whether the button is being hovered over and changes style accordingly
            # This should be placed in the control loop after if event.type==pygame.MOUSEMOTION:

            mouse_position=pygame.mouse.get_pos()
            if self.button_position.collidepoint(mouse_position):
                # print("Hovering")
                self.current_color = self.hover_color
                        
            else:
                # print("Not hovering")
                self.current_color = self.color

            self.render = self.font.render(self.button_text, True, self.text_color, self.current_color)


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