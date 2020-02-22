import arcade
from entities.entity import Entity
from util import char_to_pixel


def get_blocking_sprites(x, y, sprite_list):
    """ Given an x,y grid location, return list of sprites that block movement. """
    px, py = char_to_pixel(x, y)
    sprite_list = arcade.get_sprites_at_exact_point((px, py), sprite_list)
    blocking_sprite_list = arcade.SpriteList()
    for sprite in sprite_list:
        if isinstance(sprite, Entity):
            if sprite.blocks:
                blocking_sprite_list.append(sprite)
        else:
            raise TypeError("Sprite is not an instance of Entity.")

    if len(blocking_sprite_list) > 0:
        return blocking_sprite_list
    else:
        return None
