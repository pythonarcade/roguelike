from astar import astar

class BasicMonster:
    def __init__(self):
        self.owner = None

    def take_turn(self, target, fov_map, game_map, sprite_lists):
        results = []

        monster = self.owner
        if monster.is_visible:

            if monster.distance_to(target) >= 2:
                # monster.move_astar(target, entities, game_map)
                # monster.move_towards(target.x, target.y, game_map, entities)
                result = astar(sprite_lists, (monster.x, monster.y), (target.x, target.y))
                print(f"Path from ({monster.x}, {monster.y}) to ({target.x}, {target.y})", result)
                if result:
                    point = result[1]
                    x, y = point
                    monster.x = x
                    monster.y = y
                    print(f"Move to ({x}, {y})")
            elif target.fighter.hp > 0:
                print('The {0} insults you! Your ego is damaged!'.format(monster.name))
                # attack_results = monster.fighter.attack(target)
                # results.extend(attack_results)

        return results
