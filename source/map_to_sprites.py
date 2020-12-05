from typing import List

import arcade

from constants import *
from themes.current_theme import *

from entities.entity import Entity
from entities.lightning_scroll import LightningScroll
from entities.fireball_scroll import FireballScroll
from entities.potion import Potion
from entities.stairs import Stairs
from entities.creature_factory import get_random_monster_by_challenge
from entities.creature_factory import make_monster_sprite


def map_to_sprites(game_map: List[List[int]]) -> arcade.SpriteList:
    """ Take a grid of numbers and convert to sprites. """
    sprite_list = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=16)

    # Take the tiles and make sprites out of them
    for y in range(len(game_map[0])):
        for x in range(len(game_map)):
            sprite = None
            # print(f"{game_map[x][y]} ", end="")
            if game_map[x][y] == TILE.WALL:
                sprite = Entity(x, y, WALL_TEXTURE_ID, colors['transparent'])
                sprite.name = "Wall"
                sprite.block_sight = True
                sprite.blocks = True
                sprite.visible_color = colors["light_wall"]
                sprite.not_visible_color = colors["dark_wall"]
            elif game_map[x][y] == TILE.FLOOR:
                sprite = Entity(x, y, FLOOR_TEXTURE_ID, colors['transparent'])
                sprite.name = "Ground"
                sprite.block_sight = False
                sprite.visible_color = colors["light_ground"]
                sprite.not_visible_color = colors["dark_ground"]
            elif game_map[x][y] == TILE.STAIRS_DOWN:
                sprite = Stairs(x, y, STAIRS_DOWN_TEXTURE_ID, colors['transparent'])
                sprite.name = "Stairs Down"
                sprite.block_sight = False
                sprite.visible_color = colors["light_ground"]
                sprite.not_visible_color = colors["dark_ground"]
            elif game_map[x][y] == TILE.HEALING_POTION:
                sprite = Potion(x, y)
            elif game_map[x][y] == TILE.LIGHTNING_SCROLL:
                sprite = LightningScroll(x, y)
            elif game_map[x][y] == TILE.FIREBALL_SCROLL:
                sprite = FireballScroll(x, y)
            elif game_map[x][y]:
                raise ValueError(f"Unknown number in map: {game_map[x][y]}")

            if sprite:
                sprite_list.append(sprite)

    return sprite_list


def creatures_to_sprites(game_map: List[List[int]]) -> arcade.SpriteList:
    """ Take a grid of numbers and convert to sprites. """
    sprite_list = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=16)

    # Take the tiles and make sprites out of them
    for y in range(len(game_map[0])):
        for x in range(len(game_map)):

            if game_map[x][y]:
                m = get_random_monster_by_challenge(game_map[x][y])
                sprite = make_monster_sprite(m)
                sprite.x = x
                sprite.y = y
                sprite.alpha = 0
                sprite.visible_color = colors['monster']

                sprite_list.append(sprite)

    return sprite_list
