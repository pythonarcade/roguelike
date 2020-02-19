from astar import astar


class BasicMonster:
    def __init__(self):
        self.owner = None

    def take_turn(self, target, sprite_lists):
        results = []

        monster = self.owner
        if monster.is_visible and not monster.is_dead:

            if monster.distance_to(target) >= 2:
                result = astar(
                    sprite_lists, (monster.x, monster.y), (target.x, target.y)
                )
                # print(
                #     f"Path from ({monster.x}, {monster.y}) to ({target.x}, {target.y})",
                #     result,
                # )
                if result:
                    point = result[1]
                    x, y = point
                    monster.x = x
                    monster.y = y
                    # print(f"Move to ({x}, {y})")
            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results
