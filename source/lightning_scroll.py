import math

from typing import Optional
from constants import *
from item import Item
from entity import Entity


class LightningScroll(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x=x,
                         y=y,
                         char="S",
                         color=colors["transparent"],
                         visible_color=colors["potion"],
                         name="Lightning Scroll",
                         item=Item(),
                         )

    def use(self, game_engine: 'GameEngine'):

        # Find the closest enemy
        closest_distance: Optional[float] = None
        closest_entity: Optional[Entity] = None
        for entity in game_engine.entities:
            if entity.is_visible and entity.fighter and not entity.is_dead:
                x1 = game_engine.player.x
                y1 = game_engine.player.y
                x2 = entity.x
                y2 = entity.y
                distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                if closest_distance is None or distance < closest_distance:
                    closest_entity = entity
                    closest_distance = distance

        # If we've got a closest enemy, zap them.
        if closest_entity:
            damage = 15
            results = [{"enemy_turn": True}, {"message": f"{closest_entity.name} was struck by lighting for {damage} points."}]
            result = closest_entity.fighter.take_damage(damage)
            if result:
                results.extend(result)

            game_engine.player.inventory.remove_item(self)
            return
        else:
            return None
