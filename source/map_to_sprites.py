from typing import List

import arcade

from constants import *

from entities.entity import Entity
from entities.lightning_scroll import LightningScroll
from entities.fireball_scroll import FireballScroll
from entities.potion import Potion
from entities.orc import Orc
from entities.troll import Troll
from entities.stairs import Stairs

def map_to_sprites(game_map: List[List[int]]) -> arcade.SpriteList[Entity]:

    sprite_list = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=16)

    # Take the tiles and make sprites out of them
    for y in range(len(game_map[0])):
        for x in range(len(game_map)):
            sprite = None
            # print(f"{game_map[x][y]} ", end="")
            if game_map[x][y] == TILE_WALL:
                sprite = Entity(x, y, WALL_TEXTURE_ID, arcade.csscolor.BLACK)
                sprite.name = "Wall"
                sprite.block_sight = True
                sprite.blocks = True
                sprite.visible_color = colors["light_wall"]
                sprite.not_visible_color = colors["dark_wall"]
            elif game_map[x][y] == TILE_FLOOR:
                sprite = Entity(x, y, WALL_TEXTURE_ID, arcade.csscolor.BLACK)
                sprite.name = "Ground"
                sprite.block_sight = False
                sprite.visible_color = colors["light_ground"]
                sprite.not_visible_color = colors["dark_ground"]
            elif game_map[x][y] == TILE_STAIRS_DOWN:
                sprite = Stairs(x, y, STAIRS_DOWN_TEXTURE_ID, arcade.csscolor.WHITE)
                sprite.name = "Stairs Down"
                sprite.block_sight = False
                sprite.visible_color = colors["light_ground"]
                sprite.not_visible_color = colors["dark_ground"]
            elif game_map[x][y] == TILE_ORC:
                sprite = Orc(x, y)
            elif game_map[x][y] == TILE_TROLL:
                sprite = Troll(x, y)
            elif game_map[x][y] == TILE_HEALING_POTION:
                sprite = Potion(x, y)
            elif game_map[x][y] == TILE_LIGHTNING_SCROLL:
                sprite = LightningScroll(x, y)
            elif game_map[x][y] == TILE_FIREBALL_SCROLL:
                sprite = FireballScroll(x, y)

            if sprite:
                sprite_list.append(sprite)
        # print()

    return sprite_list
