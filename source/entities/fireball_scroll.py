from constants import *
from themes.current_theme import *
from entities.item import Item
from entities.entity import Entity
from util import char_to_pixel


class FireballScroll(Entity):
    def __init__(self, x: int = 0, y: int = 0):
        self.game_engine = None

        super().__init__(
            x=x,
            y=y,
            texture_id=SCROLL_TEXTURE_ID,
            color=colors["transparent"],
            visible_color=colors["potion"],
            name="Fireball Scroll",
            item=Item(),
        )
        self.sound = arcade.load_sound("sounds/explosion2.ogg")


    def use(self, game_engine: "GameEngine"):
        print("Use")
        self.game_engine = game_engine
        game_engine.game_state = SELECT_LOCATION
        game_engine.grid_select_handlers.append(self.click)
        return None

    def apply_damage(self, grid_x, grid_y, amount, results):
        pixel_x, pixel_y = char_to_pixel(grid_x, grid_y)
        sprites = arcade.get_sprites_at_point(
            (pixel_x, pixel_y), self.game_engine.cur_level.creatures
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
        """
        Process a click with where we should place the fireball
        """
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

        arcade.play_sound(self.sound)

        self.game_engine.player.inventory.remove_item(self)
        self.game_engine.game_state = NORMAL

        results.extend([{"enemy_turn": True}])
        return results
