"""
Fighter class manages any entity, including the player, that can fight.
"""


class Fighter:
    """ Manage fighting player or NPC """

    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.owner = None

    def take_damage(self, amount):
        results = []

        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            results.append({"dead": self.owner})

        return results

    def attack(self, target):
        results = []

        damage = self.power - target.fighter.defense

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

        return results
