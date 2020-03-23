import arcade.key
from themes.current_theme import SPRITE_SCALE
from themes.current_theme import SPRITE_WIDTH
from themes.current_theme import SPRITE_HEIGHT

SCREEN_TITLE = "RogueLike"
MAP_HEIGHT = 37
MAP_WIDTH = 90

STATUS_PANEL_HEIGHT = 65
SCREEN_WIDTH = int(SPRITE_WIDTH * MAP_WIDTH * SPRITE_SCALE)
SCREEN_HEIGHT = int(SPRITE_HEIGHT * MAP_HEIGHT * SPRITE_SCALE + STATUS_PANEL_HEIGHT) + 20

FOV_RADIUS = 10
DEATH_DELAY = 0.5

REPEAT_MOVEMENT_DELAY = 0.25


class _GameState:
    NORMAL = 1
    SELECT_LOCATION = 2
    CHARACTER_SCREEN = 3


STATE = _GameState()


class _Tile:
    EMPTY = 0
    FLOOR = 1
    WALL = 2
    ORC = 3
    TROLL = 4
    LIGHTNING_SCROLL = 5
    FIREBALL_SCROLL = 6
    HEALING_POTION = 7
    STAIRS_DOWN = 8


TILE = _Tile()


KEYMAP_UP = [arcade.key.UP, arcade.key.NUM_8]
KEYMAP_LEFT = [arcade.key.LEFT, arcade.key.NUM_4]
KEYMAP_DOWN = [arcade.key.DOWN, arcade.key.NUM_2]
KEYMAP_RIGHT = [arcade.key.RIGHT, arcade.key.NUM_6]
KEYMAP_UP_LEFT = [arcade.key.NUM_7]
KEYMAP_DOWN_LEFT = [arcade.key.NUM_1]
KEYMAP_UP_RIGHT = [arcade.key.NUM_9]
KEYMAP_DOWN_RIGHT = [arcade.key.NUM_3]
KEYMAP_PICKUP = [arcade.key.NUM_5, arcade.key.G]
KEYMAP_SELECT_ITEM_1 = [arcade.key.KEY_1]
KEYMAP_SELECT_ITEM_2 = [arcade.key.KEY_2]
KEYMAP_SELECT_ITEM_3 = [arcade.key.KEY_3]
KEYMAP_SELECT_ITEM_4 = [arcade.key.KEY_4]
KEYMAP_SELECT_ITEM_5 = [arcade.key.KEY_5]
KEYMAP_SELECT_ITEM_6 = [arcade.key.KEY_6]
KEYMAP_SELECT_ITEM_7 = [arcade.key.KEY_7]
KEYMAP_SELECT_ITEM_8 = [arcade.key.KEY_8]
KEYMAP_SELECT_ITEM_9 = [arcade.key.KEY_9]
KEYMAP_SELECT_ITEM_0 = [arcade.key.KEY_0]
KEYMAP_USE_ITEM = [arcade.key.U]
KEYMAP_DROP_ITEM = [arcade.key.D]
KEYMAP_CHARACTER_SCREEN = [arcade.key.C]
KEYMAP_USE_STAIRS = [arcade.key.ENTER]
KEYMAP_CANCEL = [arcade.key.ESCAPE]

# Tile Types


EXPERIENCE_PER_LEVEL = [650, 1500, 2500, 4000]
