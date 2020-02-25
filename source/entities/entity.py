"""
Entities are Sprites with extra attributes set up for
the game
"""
import math
from constants import *
from util import char_to_pixel

# Load  the textures our sprites use on game start-up.
textures = arcade.load_spritesheet(
    ":resources:images/spritesheets/codepage_437.png",
    sprite_width=SPRITE_WIDTH,
    sprite_height=SPRITE_HEIGHT,
    columns=32,
    count=8 * 32,
)


class Entity(arcade.Sprite):
    """ On-screen sprite represented by some Code Page 437 character """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: str = "X",
        color=arcade.csscolor.WHITE,
        visible_color=arcade.csscolor.WHITE,
        not_visible_color=arcade.csscolor.WHITE,
        name=None,
        blocks=False,
        fighter=None,
        ai=None,
        inventory=None,
        item=None,
    ):
        super().__init__(scale=SPRITE_SCALE)

        # Set the internal variables, before we try setting via the
        # setter.
        self._x = 0
        self._y = 0
        self._char_value = 0

        self.x = x
        self.y = y
        self.char = char

        self.color = color
        self.visible_color = visible_color
        self.not_visible_color = not_visible_color

        self.name = name
        self.blocks = blocks
        self.block_sight = False
        self.is_visible = False
        self.is_dead = False
        self.item = item
        self.inventory = inventory

        # Fighters have HP and can do damage
        self.fighter = fighter
        if self.fighter:
            self.fighter.owner = self

        # Any entity with AI to move around gets one of these
        self.ai = ai
        if self.ai:
            self.ai.owner = self

    def get_dict(self):
        result = {}
        result['x'] = self.x
        result['y'] = self.y
        result['visible_color'] = self.visible_color
        result['not_visible_color'] = self.not_visible_color
        result['alpha'] = self.alpha
        result['color'] = self.color
        result['char'] = self.char
        result['name'] = self.name
        result['blocks'] = self.blocks
        result['block_sight'] = self.block_sight
        result['is_visible'] = self.is_visible
        result['is_dead'] = self.is_dead
        if self.ai:
            result['ai'] = True
        if self.fighter:
            result['fighter'] = self.fighter.get_dict()
        if self.item:
            result['item'] = True
        if self.inventory:
            result['inventory'] = self.inventory.get_dict()

        return result

    def restore_from_dict(self, result):
        """
        Fill in the fields for this entity based on a dict. Used in serializing
        the object to disk or over a network.
        """
        from entities.fighter import Fighter
        from entities.ai import BasicMonster
        from entities.item import Item
        from entities.inventory import Inventory

        self.x = result['x']
        self.y = result['y']
        self.visible_color = result['visible_color']
        self.not_visible_color = result['not_visible_color']
        self.color = result['color']
        self.alpha = result['alpha']
        self.char = result['char']
        self.name = result['name']
        self.blocks = result['blocks']
        self.block_sight = result['block_sight']
        self.is_visible = result['is_visible']
        self.is_dead = result['is_dead']
        if 'item' in result:
            self.item = Item()
            print(f"Restore item {self.name}")
        if 'ai' in result:
            self.ai = BasicMonster()
            self.ai.owner = self
        self.inventory = None
        if 'fighter' in result:
            self.fighter = Fighter()
            self.fighter.owner = self
            self.fighter.restore_from_dict(result['fighter'])
        if 'inventory' in result:
            self.inventory = Inventory()
            self.inventory.restore_from_dict(result['inventory'])

    def move(self, delta_x, delta_y):
        # Move the entity by a given amount
        self.x += delta_x
        self.y += delta_y

    def distance_to(self, other):
        """
        Find the distance to another sprite
        """
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
        self._char_value = value
        self.texture = textures[self._char_value]

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.center_x, self.center_y = char_to_pixel(self._x, self._y)
        # self.center_x = self._x * SPRITE_WIDTH * SCALE + SPRITE_WIDTH / 2 * SCALE

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.center_x, self.center_y = char_to_pixel(self._x, self._y)
        # self.center_y = self._y * SPRITE_HEIGHT * SCALE + SPRITE_HEIGHT / 2 * SCALE
