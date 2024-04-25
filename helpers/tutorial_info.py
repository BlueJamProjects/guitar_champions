import partials.tutorial_popup.tutorial_popup as tutorial_popup


class TutorialInfo(object):

    """
    Represents information about a tutorial, including popups and sprites.

    Args:
        popup_list (list, optional): A list of TutorialPopup objects representing popups. Default is an empty list.
        sprites_list (list, optional): A list of lists of SpriteItem objects representing sprite screens. Default is an empty list.

    Attributes:
        current_popup (TutorialPopup): The current popup being displayed.
        current_sprites (list): The list of sprites currently displayed on the screen.
        popup_index (int): The index of the current popup in the `popup_list`.
        sprites_index (int): The index of the current sprites screen in the `sprites_list`.
        popup_list (list): A list of TutorialPopup objects.
        sprites_list (list): A list of lists of SpriteItem objects, each representing a screen of sprites.

    Note:
        `popup_list` and `sprites_list` should have the same number of elements or issues may arise.

    Methods:
        next(): Sets the current_popup and current_sprites to the next one in the list.
            Prints a message if reaching the end of popups or sprites list.
        
        previous(): Sets the current_popup and current_sprites to the previous one in the list.
            Prints a message if reaching the beginning of popups or sprites list.
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
        Moves to the next popup and sprite screen in the respective lists.

        Updates the current_popup and current_sprites attributes to the next elements in their respective lists.

        If there are more popups to navigate, updates the popup index and sets the number of the current popup.

        If there are more sprite screens to navigate, updates the sprites index.

        If there are no more popups or sprite screens to navigate, prints a message indicating the end.
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
        Sets the current_popup and current_sprites to the previous ones in their respective lists.

        If there are previous popups or sprites screens available, updates the indices and sets the current ones accordingly.
        If already at the beginning of either list, prints a message indicating so.

        Returns:
            None
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