from typing import Optional

from constants import *
from inventory import Inventory
from entities.entity import Entity
from entities.potion import Potion
from entities.fireball_scroll import FireballScroll
from entities.orc import Orc
from entities.troll import Troll
from entities.lightning_scroll import LightningScroll
from procedural_generation.game_map import GameMap
from entities.fighter import Fighter
from recalculate_fov import recalculate_fov
from get_blocking_sprites import get_blocking_sprites
from map_to_sprites import map_to_sprites

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
        self.game_state = NORMAL
        self.grid_select_handlers = []

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
        self.game_map.make_map(player=self.player)

        self.dungeon_sprites = map_to_sprites(self.game_map.tiles)
        self.entities = map_to_sprites(self.game_map.entities)

        # Set field of view
        recalculate_fov(
            self.player.x,
            self.player.y,
            FOV_RADIUS,
            [self.dungeon_sprites, self.entities],
        )

    def get_entity_dict(self, entity):
        name = entity.__class__.__name__
        return {name: entity.get_dict()}

    def get_dict(self):

        player_dict = self.get_entity_dict(self.player)

        dungeon_dict = []
        for sprite in self.dungeon_sprites:
            dungeon_dict.append(self.get_entity_dict(sprite))

        entity_dict = []
        for sprite in self.entities:
            entity_dict.append(self.get_entity_dict(sprite))

        result = {'player': player_dict,
                  'dungeon': dungeon_dict,
                  'entities': entity_dict}
        return result

    def restore_from_dict(self, data):

        self.dungeon_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=16
        )
        self.entities = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=16
        )

        player_dict = data['player']
        self.player.restore_from_dict(player_dict['Entity'])

        for entity_dict in data['dungeon']:
            entity_name = list(entity_dict.keys())[0]
            if entity_name == 'Entity':
                entity = Entity()
                entity.restore_from_dict(entity_dict[entity_name])
                self.dungeon_sprites.append(entity)

        for entity_dict in data['entities']:
            entity_name = list(entity_dict.keys())[0]
            if entity_name == 'Potion':
                entity = Potion()
            elif entity_name == 'FireballScroll':
                entity = FireballScroll()
            elif entity_name == 'LightningScroll':
                entity = LightningScroll()
            elif entity_name == 'Orc':
                entity = Orc()
            elif entity_name == 'Troll':
                entity = Troll()
            else:
                print(f"Error, don't know how to restore {entity_name}.")

            entity.restore_from_dict(entity_dict[entity_name])
            self.dungeon_sprites.append(entity)

    def grid_click(self, grid_x, grid_y):
        for f in self.grid_select_handlers:
            results = f(grid_x, grid_y)
            if results:
                self.action_queue.extend(results)
        self.grid_select_handlers = []

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
            results = [{"enemy_turn": True}]
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

    def dying(self, target: Entity):
        target.color = colors["dying"]
        # target.visible_color = colors["dying"]
        target.is_dead = True
        if target is self.player:
            results = [{"message": "Player has died!"}]
        else:
            results = [
                {"message": f"{target.name} has been killed!"},
                {"delay": {"time": DEATH_DELAY, "action": {"dead": target}}},
            ]
        return results

    def pick_up(self):
        entities = arcade.get_sprites_at_exact_point(
            self.player.position, self.entities
        )
        for entity in entities:
            if isinstance(entity, Entity):
                if entity.item:
                    results = self.player.inventory.add_item(entity)
                    return results
            else:
                raise ValueError("Sprite is not an instance of Entity.")
        return None

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
            if "dying" in action:
                target = action["dying"]
                new_actions = self.dying(target)
                if new_actions:
                    new_action_queue.extend(new_actions)
            if "dead" in action:
                target = action["dead"]
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
                new_actions = self.pick_up()
                if new_actions:
                    new_action_queue.extend(new_actions)

            if "select_item" in action:
                item_number = action["select_item"]
                if 1 <= item_number <= self.player.inventory.capacity:
                    # Fix up for 0 based index
                    if self.selected_item != item_number - 1:
                        self.selected_item = item_number - 1
                        new_action_queue.extend({"enemy_turn": True})

            if "use_item" in action:
                item_number = self.selected_item
                if item_number is not None:
                    item = self.player.inventory.get_item_number(item_number)
                    if item:
                        results = item.use(self)
                        if results:
                            new_action_queue.extend(results)

            if "drop_item" in action:
                item_number = self.selected_item
                if item_number is not None:
                    item = self.player.inventory.get_item_number(item_number)
                    if item:
                        self.player.inventory.remove_item_number(item_number)
                        self.entities.append(item)
                        item.center_x = self.player.center_x
                        item.center_y = self.player.center_y
                        new_action_queue.extend(
                            [{"message": f"You dropped the {item.name}."}]
                        )

        # Reload the action queue with new items
        self.action_queue = new_action_queue
