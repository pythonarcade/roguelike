import arcade.key

SCREEN_TITLE = "RogueLike"
SCALE = 1
SPRITE_WIDTH = 9
SPRITE_HEIGHT = 16
MAP_HEIGHT = 45
MAP_WIDTH = 80
STATUS_PANEL_HEIGHT = 40
SCREEN_WIDTH = SPRITE_WIDTH * MAP_WIDTH
SCREEN_HEIGHT = SPRITE_HEIGHT * MAP_HEIGHT + STATUS_PANEL_HEIGHT
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


colors = {
    "dark_wall": (0, 0, 100, 255),
    "dark_ground": (50, 50, 150, 255),
    "light_wall": (130, 110, 50, 255),
    "light_ground": (200, 180, 50, 255),
    "status_panel_background": (200, 180, 50, 255),
    "status_panel_text": (0, 0, 0, 255),
    "desaturated_green": (63, 127, 63, 255),
    "darker_green": (0, 127, 0, 255),
    "dying": (200, 0, 0, 255),
    "dead_body": (127, 0, 0, 255),
    "transparent": (0, 0, 0, 0),
    "status_bar_background": (80, 0, 0, 255),
    "status_bar_foreground": (255, 0, 0, 255),
}
