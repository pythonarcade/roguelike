from entities.entity import Entity
from entities.fighter import Fighter
from entities.ai import BasicMonster
from constants import colors


class Orc(Entity):
    def __init__(self, x: int = 0, y: int = 0):
        fighter_component = Fighter(hp=10, defense=0, power=3)
        ai_component = BasicMonster()
        super().__init__(
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
