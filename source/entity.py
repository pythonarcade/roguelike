import math
import arcade
from constants import *
from util import get_blocking_sprites

textures = arcade.load_spritesheet(
    ":resources:images/spritesheets/codepage_437.png",
    sprite_width=SPRITE_WIDTH,
    sprite_height=SPRITE_HEIGHT,
    columns=32,
    count=8 * 32,
)


class Entity(arcade.Sprite):
    """ Character Sprite on Screen """

    def __init__(
        self,
        x: int,
        y: int,
        char: str = "X",
        color=arcade.csscolor.WHITE,
        visible_color=arcade.csscolor.WHITE,
        not_visible_color=arcade.csscolor.WHITE,
        name=None,
        blocks=False,
        fighter=None,
        ai=None,
    ):
        super().__init__(scale=SCALE)
        self.x = x
        self.y = y
        self.visible_color = visible_color
        self.not_visible_color = not_visible_color
        self.color = color
        self.char = char
        self.name = name
        self.blocks = blocks
        self.block_sight = False
        self.is_visible = False
        self.is_dead = False

        self.fighter = fighter
        if self.fighter:
            self.fighter.owner = self

        self.ai = ai
        if self.ai:
            self.ai.owner = self

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (
            game_map.is_blocked(self.x + dx, self.y + dy)
            or get_blocking_sprites(self.x + dx, self.y + dy, entities)
        ):
            self.move(dx, dy)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

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
