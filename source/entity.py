import arcade
from constants import *

textures = arcade.load_spritesheet(
    ":resources:images/spritesheets/codepage_437.png",
    sprite_width=SPRITE_WIDTH,
    sprite_height=SPRITE_HEIGHT,
    columns=32,
    count=8 * 32,
)

class Entity(arcade.Sprite):
    """ Character Sprite on Screen """

    def __init__(self, x:int, y:int, char:str="X", color=arcade.csscolor.WHITE):
        super().__init__(scale=SCALE)
        self.x = x
        self.y = y
        self.color = color
        self.char = char
        self.name = ""
        self.blocks = False
        self.block_sight = False
        self.is_visible = False

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    @property
    def char(self):
        """ Character of the item """
        return chr(self._char_value)

    @char.setter
    def char(self, value):
        self._char_value = ord(value)
        self.texture = textures[self._char_value]

    @property
    def char_value(self):
        """ Character of the item """
        return self._char_value

    @char_value.setter
    def char_value(self, value):
        self._char = value
        self.texture = textures[self._char_value]

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.center_x = self._x * SPRITE_WIDTH * SCALE + SPRITE_WIDTH / 2 * SCALE

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.center_y = self._y * SPRITE_HEIGHT * SCALE + SPRITE_HEIGHT / 2 * SCALE
