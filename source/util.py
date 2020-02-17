from constants import *


def char_to_pixel(char_x, char_y):
    px = char_x * SPRITE_WIDTH * SCALE + SPRITE_WIDTH / 2 * SCALE
    py = char_y * SPRITE_HEIGHT * SCALE + SPRITE_HEIGHT / 2 * SCALE
    return px, py


def pixel_to_char(pixel_x, pixel_y):
    px = pixel_x - SPRITE_WIDTH / 2 * SCALE
    px = round(px / (SPRITE_WIDTH * SCALE))

    py = pixel_y - SPRITE_HEIGHT / 2 * SCALE
    py = round(py / SPRITE_HEIGHT * SCALE)
    return px, py
