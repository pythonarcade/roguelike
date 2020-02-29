"""
Fighter class manages any entity, including the player, that can fight.
"""
from typing import Optional
from entities.entity import Entity
import random


class Fighter:
    """ Manage fighting player or NPC """

    def __init__(self, hp=0, defense=0, power=0, xp_reward=0, current_xp=0, level=0, ability_points=0):
        self.max_hp: int = hp
        self.hp: int = hp
        self.defense: int = defense
        self.power: int = power
        self.owner: Optional[Entity] = None
        self.xp_reward: int = xp_reward
        self.current_xp: int = current_xp
        self.level: int = level
        self.ability_points: int = ability_points

    def get_dict(self):
        result = {'max_hp': self.max_hp,
                  'hp': self.hp,
                  'defense': self.defense,
                  'power': self.power,
                  'xp_reward': self.xp_reward,
                  'current_xp': self.current_xp,
                  'level': self.level,
                  'ability_points': self.ability_points
                  }
        return result

    def restore_from_dict(self, result):
        self.max_hp = result['max_hp']
        self.hp = result['hp']
        self.defense = result['defense']
        self.power = result['power']
        self.xp_reward = result['xp_reward']
        self.current_xp = result['current_xp']
        self.level = result['level']
        self.ability_points = result['ability_points']

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

        # Character will have a level, don't make a noise for the character.
        if self.level == 0:
            monster_delay_sound = random.randrange(20) * 0.01 + 0.05
            results.append({"delay": {"time": monster_delay_sound, "action": {"play_sound": "monster_attack"}}})
            print("Monster attack queued")

        if damage > 0:
            results.append(
                {
                    "message": f"{self.owner.name.capitalize()} attacks {target.name} for {damage} hit points."
                }
            )
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append(
                {
                    "message": f"{self.owner.name.capitalize()} attacks {target.name} but does no damage."
                }
            )

        print("Returning from attack: ", results)
        return results
