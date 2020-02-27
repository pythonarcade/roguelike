"""
Entities are Sprites with extra attributes set up for
the game
"""
import math
from constants import *
from themes.current_theme import textures
from util import char_to_pixel


class Entity(arcade.Sprite):
    """ On-screen sprite """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        texture_id: int = 0,
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
        self._texture_id = 0

        self.x = x
        self.y = y
        self.texture_id = texture_id

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
        result['texture_id'] = self.texture_id
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
        self.texture_id = result['texture_id']
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
    def texture_id(self):
        """ Texture id of the item """
        return self._texture_id

    @texture_id.setter
    def texture_id(self, value):
        self._texture_id = value
        self.texture = textures[self._texture_id]

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
