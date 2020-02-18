
class BasicMonster:
    def __init__(self):
        self.owner = None

    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        monster = self.owner
        if monster.is_visible:

            if monster.distance_to(target) >= 2:
                # monster.move_astar(target, entities, game_map)
                monster.move_towards(target.x, target.y, game_map, entities)

            elif target.fighter.hp > 0:
                print('The {0} insults you! Your ego is damaged!'.format(monster.name))
                # attack_results = monster.fighter.attack(target)
                # results.extend(attack_results)

        return results
