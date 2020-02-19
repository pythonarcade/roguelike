from entity import Entity

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item:Entity):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'message': 'You cannot carry any more, your inventory is full'
            })
        else:
            results.append({
                'message': f'You pick up the {item.name}!'
            })
            item.remove_from_sprite_lists()
            self.items.append(item)

        return results