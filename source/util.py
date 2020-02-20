from constants import *
from entity import Entity
import arcade


def char_to_pixel(char_x, char_y):
    px = char_x * SPRITE_WIDTH * SPRITE_SCALE + SPRITE_WIDTH / 2 * SPRITE_SCALE
    py = (
        char_y * SPRITE_HEIGHT * SPRITE_SCALE + SPRITE_HEIGHT / 2 * SPRITE_SCALE
    ) + STATUS_PANEL_HEIGHT
    return px, py


def pixel_to_char(pixel_x, pixel_y):
    px = pixel_x - SPRITE_WIDTH / 2 * SPRITE_SCALE
    px = round(px / (SPRITE_WIDTH * SPRITE_SCALE))

    py = pixel_y - SPRITE_HEIGHT / 2 * SPRITE_SCALE
    py = round(py / SPRITE_HEIGHT * SPRITE_SCALE) - STATUS_PANEL_HEIGHT
    return px, py


def get_blocking_sprites(x, y, sprite_list):
    """ Given an x,y grid location, return list of sprites that block movement. """
    px, py = char_to_pixel(x, y)
    sprite_list = arcade.get_sprites_at_exact_point((px, py), sprite_list)
    for sprite in sprite_list:
        if isinstance(sprite, Entity):
            if not sprite.blocks:
                sprite_list.remove(sprite)
        else:
            raise TypeError("Sprite is not an instance of Entity." "")
    if len(sprite_list) > 0:
        return sprite_list
    else:
        return None
