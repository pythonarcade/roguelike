from constants import *
from entities.item import Item
from entities.entity import Entity
from util import char_to_pixel


class FireballScroll(Entity):
    def __init__(self, x: int, y: int):
        self.game_engine = None

        super().__init__(
            x=x,
            y=y,
            char="S",
            color=colors["transparent"],
            visible_color=colors["potion"],
            name="Fireball Scroll",
            item=Item(),
        )

    def use(self, game_engine: "GameEngine"):
        print("Use")
        self.game_engine = game_engine
        game_engine.game_state = SELECT_LOCATION
        game_engine.grid_select_handlers.append(self.click)
        return None

    def apply_damage(self, grid_x, grid_y, amount, results):
        pixel_x, pixel_y = char_to_pixel(grid_x, grid_y)
        sprites = arcade.get_sprites_at_point(
            (pixel_x, pixel_y), self.game_engine.entities
        )
        for sprite in sprites:
            if sprite.fighter and not sprite.is_dead:
                results.extend(
                    [
                        {
                            "message": f"{sprite.name} was struck by a fireball for {amount} points."
                        }
                    ]
                )
                result = sprite.fighter.take_damage(amount)
                if result:
                    results.extend(result)

    def click(self, x, y):
        print("Click!", x, y)
        results = []
        self.apply_damage(x, y, 10, results)

        self.apply_damage(x - 1, y - 1, 8, results)
        self.apply_damage(x, y - 1, 8, results)
        self.apply_damage(x + 1, y - 1, 8, results)

        self.apply_damage(x - 1, y, 8, results)
        self.apply_damage(x + 1, y, 8, results)

        self.apply_damage(x - 1, y + 1, 8, results)
        self.apply_damage(x, y + 1, 8, results)
        self.apply_damage(x + 1, y + 1, 8, results)

        self.game_engine.player.inventory.remove_item(self)
        results.extend([{"enemy_turn": True}])
        return results
