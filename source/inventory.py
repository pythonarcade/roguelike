"""
Manage inventory for the character.
"""
from entity import Entity


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = [None for _ in range(self.capacity)]

    def add_item(self, item: Entity):
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

        return results

    def get_item_number(self, item: int):
        return self.items[item]

    def remove_item_number(self, item: int):
        results = []
        self.items[item] = None
        return results
