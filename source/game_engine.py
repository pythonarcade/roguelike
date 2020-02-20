from typing import Optional

from constants import *
from inventory import Inventory
from entity import Entity
from game_map import GameMap
from fighter import Fighter
from recalculate_fov import recalculate_fov
from get_blocking_sprites import get_blocking_sprites


class GameEngine:
    def __init__(self):
        self.characters: Optional[arcade.SpriteList] = None
        self.dungeon_sprites: Optional[arcade.SpriteList] = None
        self.entities: Optional[arcade.SpriteList] = None
        self.player: Optional[arcade.Sprite] = None
        self.game_map: Optional[GameMap] = None
        self.messages = []
        self.action_queue = []
        self.selected_item: Optional[int] = None

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # Set game state
        # Create sprite lists
        self.characters = arcade.SpriteList()
        self.dungeon_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=16
        )
        self.entities = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=16
        )

        # Create player
        fighter_component = Fighter(hp=30, defense=2, power=5)
        self.player = Entity(
            x=0,
            y=0,
            char="@",
            color=arcade.csscolor.WHITE,
            fighter=fighter_component,
            name="Player",
            inventory=Inventory(capacity=5),
        )
        self.characters.append(self.player)

        # --- Create map
        # Size of the map
        map_width = MAP_WIDTH
        map_height = MAP_HEIGHT

        self.game_map = GameMap(map_width, map_height)
        self.game_map.make_map(
            max_rooms=MAX_ROOMS,
            room_min_size=ROOM_MIN_SIZE,
            room_max_size=ROOM_MAX_SIZE,
            map_width=map_width,
            map_height=map_height,
            player=self.player,
            entities=self.entities,
            max_monsters_per_room=MAX_MONSTERS_PER_ROOM,
            max_items_per_room=MAX_ITEMS_PER_ROOM,
        )

        # Take the tiles and make sprites out of them
        for y in range(self.game_map.height):
            for x in range(self.game_map.width):
                wall = self.game_map.tiles[x][y].block_sight
                sprite = Entity(x, y, WALL_CHAR, arcade.csscolor.BLACK)
                if wall:
                    sprite.name = "Wall"
                    sprite.block_sight = True
                    sprite.blocks = True
                    sprite.visible_color = colors["light_wall"]
                    sprite.not_visible_color = colors["dark_wall"]
                else:
                    sprite.name = "Ground"
                    sprite.block_sight = False
                    sprite.visible_color = colors["light_ground"]
                    sprite.not_visible_color = colors["dark_ground"]

                self.dungeon_sprites.append(sprite)

        # Set field of view
        recalculate_fov(
            self.player.x,
            self.player.y,
            FOV_RADIUS,
            [self.dungeon_sprites, self.entities],
        )

    def move_player(self, cx, cy):
        """ Process player movement """

        # See what grid location we'd move to
        nx = self.player.x + cx
        ny = self.player.y + cy

        # See if there are walls or blocking entities there
        blocking_dungeon_sprites = get_blocking_sprites(nx, ny, self.dungeon_sprites)
        blocking_entity_sprites = get_blocking_sprites(nx, ny, self.entities)

        if not blocking_dungeon_sprites and not blocking_entity_sprites:
            # Nothing is blocking us, we can move
            self.player.x += cx
            self.player.y += cy

            # Figure out our field-of-view
            recalculate_fov(
                self.player.x,
                self.player.y,
                FOV_RADIUS,
                [self.dungeon_sprites, self.entities],
            )

            # Let the enemies move
            results = [{"enemy_turn": True}]
            self.action_queue.extend(results)

        elif blocking_entity_sprites:
            # Can't move that way, but there is a monster there.
            # Attack it.
            target = blocking_entity_sprites[0]
            results = self.player.fighter.attack(target)
            self.action_queue.extend(results)

    def move_enemies(self):
        """ Process enemy movement. """
        full_results = []
        for entity in self.entities:
            if entity.ai:
                results = entity.ai.take_turn(
                    target=self.player,
                    sprite_lists=[self.dungeon_sprites, self.entities],
                )
                full_results.extend(results)
        return full_results

    def process_action_queue(self, delta_time: float):
        new_action_queue = []
        for action in self.action_queue:
            if "enemy_turn" in action:
                new_actions = self.move_enemies()
                if new_actions:
                    new_action_queue.extend(new_actions)
            if "message" in action:
                print(action["message"])
                self.messages.append(action["message"])
            if "dead" in action:
                target = action["dead"]
                target.color = colors["dying"]
                # target.visible_color = colors["dying"]
                target.is_dead = True
                if target is self.player:
                    new_action_queue.extend([{"message": "Player has died!"}])
                else:
                    new_action_queue.extend(
                        [{"message": f"{target.name} has been killed!"}]
                    )
                    new_action_queue.extend(
                        [{"delay": {"time": DEATH_DELAY, "action": {"remove": target}}}]
                    )
            if "remove" in action:
                target = action["remove"]
                target.char = "X"
                target.color = colors["dead_body"]
                target.visible_color = colors["dead_body"]
                target.blocks = False
            if "delay" in action:
                target = action["delay"]
                target["time"] -= delta_time
                if target["time"] > 0:
                    new_action_queue.extend([{"delay": target}])
                else:
                    new_action_queue.extend([target["action"]])
            if "pickup" in action:
                entities = arcade.get_sprites_at_exact_point(
                    self.player.position, self.entities
                )
                for entity in entities:
                    if isinstance(entity, Entity):
                        if entity.item:
                            results = self.player.inventory.add_item(entity)
                            if results:
                                new_action_queue.extend(results)
                    else:
                        raise ValueError("Sprite is not an instance of Entity.")

            if "select_item" in action:
                item_number = action["select_item"]
                if item_number >= 1 and item_number <= self.player.inventory.capacity:
                    # Fix up for 0 based index
                    if self.selected_item != item_number - 1:
                        self.selected_item = item_number - 1
                        new_action_queue.extend({"enemy_turn": True})

            if "use_item" in action:
                item_number = self.selected_item
                if item_number is not None:
                    item = self.player.inventory.get_item_number(item_number)
                    if item:
                        if item.name == "Healing Potion":
                            self.player.fighter.hp += 5
                            if self.player.fighter.hp > self.player.fighter.max_hp:
                                self.player.fighter.hp = self.player.fighter.max_hp
                            self.player.inventory.remove_item_number(item_number)

                            new_action_queue.extend({"enemy_turn": True})

            if "drop_item" in action:
                item_number = self.selected_item
                if item_number is not None:
                    item = self.player.inventory.get_item_number(item_number)
                    if item:
                        self.player.inventory.remove_item_number(item_number)
                        self.entities.append(item)
                        item.center_x = self.player.center_x
                        item.center_y = self.player.center_y
                        new_action_queue.extend([{"message": f"You dropped the {item.name}."}])

        # Reload the action queue with new items
        self.action_queue = new_action_queue
