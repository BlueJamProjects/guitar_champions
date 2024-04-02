import partials.tutorial_popup.tutorial_popup as tutorial_popup


class TutorialInfo(object):
    """
    A class to store the prites for the screens for each tutorial
    """
    def __init__(self, popup_list = [], sprites_list = []):

        # IMPORTANT
        # popup_list and sprites_list should have the same amount of elements or there will be issues

        # These stores the current popup
        self.current_popup = popup_list[0]

        # This stores the list of current sprites that should be displayed on the screen
        self.current_sprites = sprites_list[0]

        # sets the number of the first popup
        self.current_popup.set_number(1, len(popup_list))

        # used to navigate the lists of popups and sprites 
        self.popup_index = 0
        self.sprites_index = 0

        # a list of  TutorialPopup objects
        self.popup_list = popup_list

        # A list of lists of SpriteItem objects
        # Each inner list will be a screen of Sprites that displays
        self.sprites_list = sprites_list




    def next(self):
        """
        Sets the current_popup and current_sprites to the next one in the list
        """

        # If there are more popups to go you update the popup index and current popup then set the current popup's number
        if self.popup_index < (len(self.popup_list) - 1):
            self.popup_index = self.popup_index + 1
            self.current_popup = self.popup_list[self.popup_index]
            self.current_popup.set_number(self.popup_index + 1, len(self.popup_list))
        else:
            # If there are no more popups to go then do nothing
            print("Reached the end of the popups")


        # If there are more sprites screens to go you update the sprits_index and current spriteslist 
        if self.sprites_index < (len(self.sprites_list) - 1):
            self.sprites_index = self.sprites_index + 1
            self.current_sprites = self.sprites_list[self.sprites_index]
        else:
            # If there are no more sprites list to go then do nothing
            print("Reached the end of the sprites list")


    def previous(self):
        """
        Sets the current_popup and current_sprites to the previous one in the list
        """
        # If there are more popups before to go back to you update the popup index and current popup then set the current popup's number    
        if self.popup_index > 0: 
            self.popup_index = self.popup_index - 1
            self.current_popup = self.popup_list[self.popup_index]
            self.current_popup.set_number(self.popup_index + 1, len(self.popup_list))
        else:
            # If you are at the beginning, do nothing
            print("Reached the beginning of the popups")

        # If there are more sprites screens to go you update the sprits_index and current spriteslist 
        if self.sprites_index > 0:
            self.sprites_index = self.sprites_index - 1
            self.current_sprites = self.sprites_list[self.sprites_index]
        else:
            # If you are at the beginning do nothing
            print("Reached the beginning of the sprites list")