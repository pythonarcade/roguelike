"""
Manage inventory for the character.
"""
from typing import Optional, List, Dict
from entities.entity import Entity
from entities.restore_entity import restore_entity

class Inventory:
    def __init__(self, capacity: int = 0):
        self._capacity = 0
        self.items = []
        self.capacity = capacity

        self.items: List[Optional[Entity]] = [None for _ in range(self.capacity)]

    @property
    def capacity(self):
        """ How many items can we hold """
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        self._capacity = value
        while len(self.items) < self.capacity:
            self.items.append(None)

    def get_dict(self):
        result = {}
        result['capacity'] = self.capacity
        item_dicts = []
        for item in self.items:
            if item is None:
                item_dicts.append(None)
            else:
                name = item.__class__.__name__
                item_dicts.append({name:item.get_dict()})

        result['items'] = item_dicts
        return result

    def restore_from_dict(self, result):
        self.capacity = result['capacity']
        for item_dict in result['items']:
           if item_dict is None:
               self.items.append(None)
           else:
               item = restore_entity(item_dict)
               self.items.append(item)

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
            results.append({"play_sound": "error"})
        else:
            results.append({"message": f"You pick up the {item.name}!"})
            if "Potion" in item.name:
                results.append({"play_sound": "pickup_potion"})
            if "Scroll" in item.name:
                results.append({"play_sound": "pickup_scroll"})

            item.remove_from_sprite_lists()
            results.append({"enemy_turn": True})

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
