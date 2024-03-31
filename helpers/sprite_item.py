
class SpriteItem(object):
    """
    A class to make specifying a sprite's object and it's location easier
    """

    def __init__(self, sprite, location=(0,0)):
        self.sprite = sprite
        self.location = location