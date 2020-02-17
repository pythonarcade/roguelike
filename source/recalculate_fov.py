import arcade
import math

from constants import *
from util import char_to_pixel


def recalculate_fov(char_x, char_y, radius, sprite_list):
    for sprite in sprite_list:
        if sprite.is_visible:
            sprite.is_visible = False
            if sprite.block_sight:
                sprite.color = colors.get("dark_wall")
            else:
                sprite.color = colors.get("dark_ground")

    resolution = 12
    circumference = 2 * math.pi * radius

    radians_per_point = 2 * math.pi / (circumference * resolution)
    point_count = int(round(circumference)) * resolution

    for i in range(point_count):
        radians = i * radians_per_point

        x = math.sin(radians) * radius + char_x
        y = math.cos(radians) * radius + char_y

        raychecks = radius
        for j in range(raychecks):
            v1 = char_x, char_y
            v2 = x, y
            x2, y2 = arcade.lerp_vec(v1, v2, j / raychecks)
            x2 = round(x2)
            y2 = round(y2)

            pixel_point = char_to_pixel(x2, y2)

            sprites_at_point = arcade.get_sprites_at_exact_point(
                pixel_point, sprite_list
            )
            # checks += 1
            blocked = False
            for sprite in sprites_at_point:
                sprite.is_visible = True
                if sprite.block_sight:
                    blocked = True
            if blocked:
                break

    for sprite in sprite_list:
        if sprite.is_visible and sprite.block_sight:
            sprite.color = colors["light_wall"]
        elif sprite.is_visible and not sprite.block_sight:
            sprite.color = colors["light_ground"]
