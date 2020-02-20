import arcade.key

SCREEN_TITLE = "RogueLike"
MAP_HEIGHT = 35
MAP_WIDTH = 120

# Some variables for the rooms in the map
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 35
MAX_MONSTERS_PER_ROOM = 3
MAX_ITEMS_PER_ROOM = 2

SPRITE_SCALE = 1
SPRITE_WIDTH = 9
SPRITE_HEIGHT = 16

STATUS_PANEL_HEIGHT = 60
SCREEN_WIDTH = int(SPRITE_WIDTH * MAP_WIDTH * SPRITE_SCALE)
SCREEN_HEIGHT = int(SPRITE_HEIGHT * MAP_HEIGHT * SPRITE_SCALE + STATUS_PANEL_HEIGHT)

WALL_CHAR = chr(219)
FOV_RADIUS = 10
DEATH_DELAY = 0.5

KEYMAP_UP = [arcade.key.UP, arcade.key.W, arcade.key.NUM_8]
KEYMAP_LEFT = [arcade.key.LEFT, arcade.key.A, arcade.key.NUM_4]
KEYMAP_DOWN = [arcade.key.DOWN, arcade.key.X, arcade.key.NUM_2]
KEYMAP_RIGHT = [arcade.key.RIGHT, arcade.key.D, arcade.key.NUM_6]
KEYMAP_UP_LEFT = [arcade.key.NUM_7, arcade.key.Q]
KEYMAP_DOWN_LEFT = [arcade.key.NUM_1, arcade.key.Z]
KEYMAP_UP_RIGHT = [arcade.key.NUM_9, arcade.key.E]
KEYMAP_DOWN_RIGHT = [arcade.key.NUM_3, arcade.key.C]
KEYMAP_PICKUP = [arcade.key.NUM_5, arcade.key.G]
KEYMAP_USE_ITEM_1 = [arcade.key.KEY_1]
KEYMAP_USE_ITEM_2 = [arcade.key.KEY_2]
KEYMAP_USE_ITEM_3 = [arcade.key.KEY_3]
KEYMAP_USE_ITEM_4 = [arcade.key.KEY_4]
KEYMAP_USE_ITEM_5 = [arcade.key.KEY_5]
KEYMAP_USE_ITEM_6 = [arcade.key.KEY_6]
KEYMAP_USE_ITEM_7 = [arcade.key.KEY_7]
KEYMAP_USE_ITEM_8 = [arcade.key.KEY_8]
KEYMAP_USE_ITEM_9 = [arcade.key.KEY_9]
KEYMAP_USE_ITEM_0 = [arcade.key.KEY_0]

colors = {
    "dark_wall": (0, 0, 100, 255),
    "dark_ground": (50, 50, 150, 255),
    "light_wall": (130, 110, 50, 255),
    "light_ground": (200, 180, 50, 255),
    "status_panel_background": (200, 180, 50, 255),
    "status_panel_text": (0, 0, 0, 255),
    "desaturated_green": (63, 127, 63, 255),
    "darker_green": (0, 127, 0, 255),
    "potion": (108, 0, 160, 255),
    "dying": (200, 0, 0, 255),
    "dead_body": (127, 0, 0, 255),
    "transparent": (0, 0, 0, 0),
    "status_bar_background": (80, 0, 0, 255),
    "status_bar_foreground": (255, 0, 0, 255),
}
