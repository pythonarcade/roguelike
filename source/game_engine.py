"""
Define the game engine
"""
from typing import Optional

from constants import *
from entities.stairs import Stairs
from entities.inventory import Inventory
from entities.entity import Entity
from procedural_generation.game_map import GameMap
from entities.fighter import Fighter
from recalculate_fov import recalculate_fov
from get_blocking_sprites import get_blocking_sprites
from map_to_sprites import map_to_sprites
from entities.restore_entity import restore_entity


class GameEngine:
    """
    This is the main game engine class, that manages the game and its actions.
    """
    def __init__(self):
        """ Set the game engine's attributes """
        self.characters: Optional[arcade.SpriteList] = None
        self.dungeon_sprites: Optional[arcade.SpriteList] = None
        self.entities: Optional[arcade.SpriteList] = None
        self.player: Optional[Entity] = None
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
            texture_id=PLAYER_TEXTURE_ID,
            color=arcade.csscolor.WHITE,
            fighter=fighter_component,
            name="Player",
            inventory=Inventory(capacity=5),
        )
        self.characters.append(self.player)

        self.setup_level()

    def setup_level(self):
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

    def get_dict(self):
        """
        Get a dictionary object for the entire game. Used in serializing
        the game state for saving to disk or sending over the network.
        """

        def get_entity_dict(entity: Entity):
            name = entity.__class__.__name__
            return {name: entity.get_dict()}

        player_dict = get_entity_dict(self.player)

        dungeon_dict = []
        for sprite in self.dungeon_sprites:
            dungeon_dict.append(get_entity_dict(sprite))

        entity_dict = []
        for sprite in self.entities:
            entity_dict.append(get_entity_dict(sprite))

        result = {'player': player_dict,
                  'dungeon': dungeon_dict,
                  'entities': entity_dict}
        return result

    def restore_from_dict(self, data):
        """
        Restore this object from a dictionary object. Used in recreating a game from a
        saved state, or from over the network.
        """
        self.dungeon_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=16
        )
        self.entities = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=16
        )

        player_dict = data['player']
        self.player.restore_from_dict(player_dict['Entity'])

        for entity_dict in data['dungeon']:
            entity = restore_entity(entity_dict)
            self.dungeon_sprites.append(entity)

        for entity_dict in data['entities']:
            entity = restore_entity(entity_dict)
            self.entities.append(entity)

    def grid_click(self, grid_x, grid_y):
        """ Handle a click on the grid """

        # Loop through anyone that has registered a grid-select handler
        for f in self.grid_select_handlers:
            results = f(grid_x, grid_y)
            if results:
                self.action_queue.extend(results)

        # Clear the handler queue
        self.grid_select_handlers = []

    def move_player(self, cx: int, cy: int):
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
        """
        Handle event of an entity dying
        """
        target.color = colors["dying"]
        # target.visible_color = colors["dying"]
        target.is_dead = True
        if target is self.player:
            results = [{"message": "Player has died!"}]
        else:
            # If a monster dies, set up a message and add a delay
            results = [
                {"message": f"{target.name} has been killed!"},
                {"delay": {"time": DEATH_DELAY, "action": {"dead": target}}},
            ]
        return results

    def use_stairs(self):
        # Get all the entities at this location
        entities = arcade.get_sprites_at_exact_point(
            self.player.position, self.dungeon_sprites
        )
        # For each entity
        for entity in entities:
            if isinstance(entity, Stairs):
                self.setup_level()
                return [{"message": "You went down a level."}]

        return [{"message": "There are no stairs here"}]

    def pick_up(self):
        """
        Handle a pick-up item entity request.
        """
        # Get all the entities at this location
        entities = arcade.get_sprites_at_exact_point(
            self.player.position, self.entities
        )
        print(f"There are {len(entities)} items")
        # For each entity
        for entity in entities:
            # Make sure it is an entity so type-checker is happy
            if isinstance(entity, Entity):
                # If entity is an item...
                if entity.item:
                    # Try and get it. (Inventory might be full.)
                    results = self.player.inventory.add_item(entity)
                    return results
                else:
                    print(f"Can't get {entity.name}")
            else:
                raise ValueError("Sprite is not an instance of Entity.")
        return None

    def process_action_queue(self, delta_time: float):
        """
        Process the action queue, kind of a dispatch-center for the
        game.
        """
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
                target.texture_id = DEAD_BODY_TEXTURE_ID
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

            if "use_stairs" in action:
                result = self.use_stairs()
                if result:
                    new_action_queue.extend(result)

        # Reload the action queue with new items
        self.action_queue = new_action_queue
