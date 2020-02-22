import arcade

from constants import *
from entity import Entity
from fighter import Fighter
from ai import BasicMonster
from lightning_scroll import LightningScroll
from fireball_scroll import FireballScroll
from potion import Potion
from item import Item


def map_to_sprites(game_map):

    sprite_list = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=16)

    # Take the tiles and make sprites out of them
    for y in range(len(game_map[0])):
        for x in range(len(game_map)):
            sprite = None
            # print(f"{game_map[x][y]} ", end="")
            if game_map[x][y] == TILE_WALL:
                sprite = Entity(x, y, WALL_CHAR, arcade.csscolor.BLACK)
                sprite.name = "Wall"
                sprite.block_sight = True
                sprite.blocks = True
                sprite.visible_color = colors["light_wall"]
                sprite.not_visible_color = colors["dark_wall"]
            elif game_map[x][y] == TILE_FLOOR:
                sprite = Entity(x, y, WALL_CHAR, arcade.csscolor.BLACK)
                sprite.name = "Ground"
                sprite.block_sight = False
                sprite.visible_color = colors["light_ground"]
                sprite.not_visible_color = colors["dark_ground"]
            elif game_map[x][y] == TILE_ORC:
                fighter_component = Fighter(hp=10, defense=0, power=3)
                ai_component = BasicMonster()
                sprite = Entity(
                    x=x,
                    y=y,
                    char="o",
                    color=colors["transparent"],
                    visible_color=colors["desaturated_green"],
                    not_visible_color=colors["transparent"],
                    name=f"Orc",
                    blocks=True,
                    fighter=fighter_component,
                    ai=ai_component,
                )
            elif game_map[x][y] == TILE_TROLL:
                fighter_component = Fighter(hp=16, defense=1, power=4)
                ai_component = BasicMonster()
                sprite = Entity(
                    x=x,
                    y=y,
                    char="T",
                    color=colors["transparent"],
                    visible_color=colors["darker_green"],
                    not_visible_color=colors["transparent"],
                    name=f"Troll",
                    blocks=True,
                    fighter=fighter_component,
                    ai=ai_component,
                )

            elif game_map[x][y] == TILE_HEALING_POTION:
                sprite = Potion(
                    x=x,
                    y=y,
                    char="!",
                    color=colors["transparent"],
                    visible_color=colors["potion"],
                    name="Healing Potion",
                    item=Item(),
                )
            elif game_map[x][y] == TILE_LIGHTNING_SCROLL:
                sprite = LightningScroll(x=x, y=y)
            elif game_map[x][y] == TILE_FIREBALL_SCROLL:
                sprite = FireballScroll(x=x, y=y)

            if sprite:
                sprite_list.append(sprite)
        # print()

    return sprite_list
