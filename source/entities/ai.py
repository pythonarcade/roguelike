"""
Logic for the monster's turn.
Basic artificial intelligence for monsters.
Ok, it isn't real AI, more like a placeholder.
"""
from entities.astar import astar
import random


class BasicMonster:
    def __init__(self):
        # The owner is a link-back to the monster
        self.owner = None

    def take_turn(self, target, sprite_lists):
        """
        Run monster's turn
        """
        results = []

        monster = self.owner
        # Can we see each other? Are we not dead?
        if monster.is_visible and not monster.is_dead:
            # Do we need to get closer?
            if monster.distance_to(target) >= 2:
                # Use the A-star algorithm to find a path to the player.
                result = astar(
                    sprite_lists, (monster.x, monster.y), (target.x, target.y)
                )
                # print(
                #     f"Path from ({monster.x}, {monster.y}) to ({target.x}, {target.y})",
                #     result,
                # )

                # If there is a path, move towards the user
                if result:
                    monster_delay_sound = random.randrange(20) * 0.01 + 0.05
                    point = result[1]
                    x, y = point
                    monster.x = x
                    monster.y = y
                    # print(f"Move to ({x}, {y})")
                    results.append({"delay": {"time": monster_delay_sound, "action": {"play_sound": "monster_walk"}}})
            elif target.fighter.hp > 0:
                # We are next to the user, fight them.
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results
