from entities.entity import Entity
from constants import colors
from entities.item import Item


class Potion(Entity):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(
            x,
            y,
            char="!",
            color=colors["transparent"],
            visible_color=colors["potion"],
            name="Healing Potion",
            item=Item(),
        )

    def use(self, game_engine):
        game_engine.player.fighter.hp += 5
        if game_engine.player.fighter.hp > game_engine.player.fighter.max_hp:
            game_engine.player.fighter.hp = game_engine.player.fighter.max_hp
        game_engine.player.inventory.remove_item(self)

        return [{"enemy_turn": True}]
