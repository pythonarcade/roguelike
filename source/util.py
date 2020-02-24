from constants import *


def char_to_pixel(char_x: int, char_y: int) -> (float, float):
    px = char_x * SPRITE_WIDTH * SPRITE_SCALE + SPRITE_WIDTH / 2 * SPRITE_SCALE
    py = (
        char_y * SPRITE_HEIGHT * SPRITE_SCALE + SPRITE_HEIGHT / 2 * SPRITE_SCALE
    ) + STATUS_PANEL_HEIGHT
    return px, py


def pixel_to_char(pixel_x: float, pixel_y: float) -> (int, int):
    px = pixel_x - SPRITE_WIDTH / 2 * SPRITE_SCALE
    px = round(px / (SPRITE_WIDTH * SPRITE_SCALE))

    py = pixel_y - SPRITE_HEIGHT / 2 * SPRITE_SCALE - STATUS_PANEL_HEIGHT
    py = round(py / SPRITE_HEIGHT * SPRITE_SCALE)
    return px, py
