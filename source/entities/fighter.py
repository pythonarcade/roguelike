"""
Fighter class manages any entity, including the player, that can fight.
"""
from typing import Optional
from entities.entity import Entity


class Fighter:
    """ Manage fighting player or NPC """

    def __init__(self, hp=0, defense=0, power=0, xp_reward=0, current_xp=0):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.owner: Optional[Entity] = None
        self.xp_reward = xp_reward
        self.current_xp = current_xp

    def get_dict(self):
        result = {}
        result['max_hp'] = self.max_hp
        result['hp'] = self.hp
        result['defense'] = self.defense
        result['power'] = self.power
        result['xp_reward'] = self.xp_reward
        result['current_xp'] = self.current_xp
        return result

    def restore_from_dict(self, result):
        self.max_hp = result['max_hp']
        self.hp = result['hp']
        self.defense = result['defense']
        self.power = result['power']
        self.xp_reward = result['xp_reward']
        self.current_xp = result['current_xp']

    def take_damage(self, amount):
        results = []

        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.owner.is_dead = True
            results.append({"dying": self.owner})

        return results

    def attack(self, target: Entity):
        results = []

        if target.is_dead:
            raise ValueError("Beating a dead horse exception.")

        damage = self.power - target.fighter.defense
        if damage > 0:
            results.append(
                {
                    "message": f"{self.owner.name.capitalize()} attacks {target.name} for {damage} hit points."
                }
            )
            results.extend(target.fighter.take_damage(damage))
            if target.is_dead:
                self.current_xp += target.fighter.xp_reward
        else:
            results.append(
                {
                    "message": f"{self.owner.name.capitalize()} attacks {target.name} but does no damage."
                }
            )

        return results
