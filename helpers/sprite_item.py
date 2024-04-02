
class SpriteItem(object):
    """
    A class to make specifying a sprite's object and it's location easier
    Used in the tutorials for the sprites that are rendered on the screen
    """

    def __init__(self, sprite, location=(0,0), is_box=False, box_color=(0,0,0),box_rect=(100,100,100,100)):
        # These two are used if this is not a box

        # the render item
        self.sprite = sprite
        # the location on screen where it should be rendered
        self.location = location

        # These 4 are used if this is a box

        # Set to true if, this is a box
        self.is_box = is_box
        # controls the color of the box
        self.box_color = box_color
        # controls the dimensions and location of the box
        self.box_rect = box_rect