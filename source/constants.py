SCREEN_TITLE = "RogueLike"
SCALE = 1
SPRITE_WIDTH = 9
SPRITE_HEIGHT = 16
MAP_HEIGHT = 45
MAP_WIDTH = 80
SCREEN_WIDTH = SPRITE_WIDTH * MAP_WIDTH
SCREEN_HEIGHT = SPRITE_HEIGHT * MAP_HEIGHT
WALL_CHAR = chr(219)
FOV_RADIUS = 10

colors = {
    "dark_wall": (0, 0, 100, 255),
    "dark_ground": (50, 50, 150, 255),
    "light_wall": (130, 110, 50, 255),
    "light_ground": (200, 180, 50, 255),
    "desaturated_green": (63, 127, 63, 255),
    "darker_green": (0, 127, 0, 255),
    "transparent": (255, 255, 255, 0),
}
