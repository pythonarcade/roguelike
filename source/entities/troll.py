from entities.entity import Entity
from entities.fighter import Fighter
from entities.ai import BasicMonster
from constants import colors


class Troll(Entity):
    def __init__(self, x: int = 0, y: int = 0):
        fighter_component = Fighter(hp=16, defense=1, power=4)
        ai_component = BasicMonster()
        super().__init__(
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
