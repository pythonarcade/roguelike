"""
Manage inventory for the character.
"""
from typing import Optional, List, Dict

from entities.entity import Entity


class Inventory:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: List[Optional[Entity]] = [None for _ in range(self.capacity)]

    def add_item(self, item: Entity) -> List[Optional[Dict]]:
        results = []

        item_placed = False
        for i in range(self.capacity):
            if self.items[i] is None:
                self.items[i] = item
                item_placed = True
                break

        if not item_placed:
            results.append(
                {"message": "You cannot carry any more, your inventory is full"}
            )
        else:
            results.append({"message": f"You pick up the {item.name}!"})
            item.remove_from_sprite_lists()
            results.extend({"enemy_turn": True})

        return results

    def get_item_number(self, item_number: int) -> Optional[Entity]:
        return self.items[item_number]

    def remove_item_number(self, item_number: int) -> List:
        results = []
        self.items[item_number] = None
        return results

    def remove_item(self, item: int) -> List:
        results = []
        for i in range(self.capacity):
            if self.items[i] is item:
                self.items[i] = None

        return results
