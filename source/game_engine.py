"""
Define the game engine
"""
from typing import Optional

from constants import *
from themes.current_theme import *
from entities.stairs import Stairs
from entities.inventory import Inventory
from entities.entity import Entity
from entities.fighter import Fighter
from procedural_generation.game_map import GameMap
from recalculate_fov import recalculate_fov
from get_blocking_sprites import get_blocking_sprites
from map_to_sprites import map_to_sprites
from map_to_sprites import creatures_to_sprites
from entities.restore_entity import restore_entity


class GameLevel:
    def __init__(self):
        self.dungeon_sprites: Optional[arcade.SpriteList] = None
        self.entities: Optional[arcade.SpriteList] = None
        self.creatures: Optional[arcade.SpriteList] = None
        self.level: int = 0


class GameEngine:
    """
    This is the main game engine class, that manages the game and its actions.
    """
    def __init__(self):
        """ Set the game engine's attributes """
        self.characters: Optional[arcade.SpriteList] = None

        self.levels = []
        self.cur_level_index = 0
        self.cur_level = None

        self.player: Optional[Entity] = None
        self.game_map: Optional[GameMap] = None
        self.messages = []
        self.action_queue = []
        self.selected_item: Optional[int] = None
        self.game_state = NORMAL
        self.grid_select_handlers = []

        self.walk_sound = arcade.load_sound("sounds/footstep_concrete_002.ogg")
        self.player_hit_monster_sound = arcade.load_sound("sounds/impactPunch_heavy_004.ogg")
        self.monster_attack_sound = arcade.load_sound("sounds/impactPunch_heavy_001.ogg")
        self.get_scroll_sound = arcade.load_sound("sounds/bookFlip2.ogg")
        self.get_potion_sound = arcade.load_sound("sounds/sinkWater1.ogg")
        self.level_up_sound = arcade.load_sound("sounds/powerUp1.ogg")
        self.monster_death = arcade.load_sound("sounds/knifeSlice.ogg")
        self.monster_walk_sound = arcade.load_sound("sounds/footstep04.ogg")
        self.pickup_potion_sound = arcade.load_sound("sounds/sinkWater1.ogg")
        self.pickup_scroll_sound = arcade.load_sound("sounds/bookFlip2.ogg")
        self.error_sound = arcade.load_sound("sounds/error5.ogg")
        self.heal_sound = arcade.load_sound("sounds/secret4.ogg")

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # Set game state
        # Create sprite lists
        self.characters = arcade.SpriteList()

        # Create player
        fighter_component = Fighter(hp=30, defense=2, power=5, level=1)
        self.player = Entity(
            x=0,
            y=0,
            texture_id=PLAYER_TEXTURE_ID,
            color=colors['player'],
            fighter=fighter_component,
            name="Player",
            inventory=Inventory(capacity=5),
        )
        self.characters.append(self.player)

        self.cur_level = self.setup_level(1)
        self.levels.append(self.cur_level)


    def setup_level(self, level_number):
        # --- Create map
        # Size of the map
        map_width = MAP_WIDTH
        map_height = MAP_HEIGHT

        level = GameLevel()

        self.game_map = GameMap(map_width, map_height)
        self.game_map.make_map(player=self.player, level=level_number)

        level.dungeon_sprites = map_to_sprites(self.game_map.tiles)
        level.entities = map_to_sprites(self.game_map.entities)
        level.creatures = creatures_to_sprites(self.game_map.creatures)
        level.level = level_number

        # Set field of view
        recalculate_fov(
            self.player.x,
            self.player.y,
            FOV_RADIUS,
            [level.dungeon_sprites, level.entities, level.creatures],
        )

        return level

    def get_dict(self):
        """
        Get a dictionary object for the entire game. Used in serializing
        the game state for saving to disk or sending over the network.
        """

        def get_entity_dict(entity: Entity):
            name = entity.__class__.__name__
            return {name: entity.get_dict()}

        player_dict = get_entity_dict(self.player)

        levels_dict = []
        for level in self.levels:

            dungeon_dict = []
            for sprite in level.dungeon_sprites:
                dungeon_dict.append(get_entity_dict(sprite))

            entity_dict = []
            for sprite in level.entities:
                entity_dict.append(get_entity_dict(sprite))

            creature_dict = []
            for sprite in level.creatures:
                creature_dict.append(get_entity_dict(sprite))

            level_dict = {'dungeon': dungeon_dict,
                          'entities': entity_dict,
                          'creatures': creature_dict}
            levels_dict.append(level_dict)


        result = {'player': player_dict,
                  'levels': levels_dict}

        return result

    def restore_from_dict(self, data):
        """
        Restore this object from a dictionary object. Used in recreating a game from a
        saved state, or from over the network.
        """
        player_dict = data['player']
        self.player.restore_from_dict(player_dict['Entity'])

        for level_dict in data['levels']:
            level = GameLevel()
            level.dungeon_sprites = arcade.SpriteList(
                use_spatial_hash=True, spatial_hash_cell_size=16
            )
            level.entities = arcade.SpriteList(
                use_spatial_hash=True, spatial_hash_cell_size=16
            )
            level.creatures = arcade.SpriteList(
                use_spatial_hash=True, spatial_hash_cell_size=16
            )

            for entity_dict in level_dict['dungeon']:
                entity = restore_entity(entity_dict)
                level.dungeon_sprites.append(entity)

            for entity_dict in level_dict['entities']:
                entity = restore_entity(entity_dict)
                level.entities.append(entity)

            for creature_dict in level_dict['creatures']:
                creature = restore_entity(creature_dict)
                level.creatures.append(creature)

            self.levels.append(level)

        self.cur_level = self.levels[-1]

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
        blocking_dungeon_sprites = get_blocking_sprites(nx, ny, self.cur_level.dungeon_sprites)
        blocking_entity_sprites = get_blocking_sprites(nx, ny, self.cur_level.creatures)

        if not blocking_dungeon_sprites and not blocking_entity_sprites:
            # Nothing is blocking us, we can move
            self.player.x += cx
            self.player.y += cy

            self.walk_sound.play()

            # Figure out our field-of-view
            recalculate_fov(
                self.player.x,
                self.player.y,
                FOV_RADIUS,
                [self.cur_level.dungeon_sprites, self.cur_level.creatures, self.cur_level.entities],
            )

            # Let the enemies move
            results = [{"enemy_turn": True}]
            self.action_queue.extend(results)

        elif blocking_entity_sprites:
            # Can't move that way, but there is a monster there.
            # Attack it.
            target = blocking_entity_sprites[0]
            if target.fighter and not target.is_dead:
                results = self.player.fighter.attack(target)
                arcade.play_sound(self.player_hit_monster_sound)
                self.action_queue.extend(results)
                results = [{"enemy_turn": True}]
                self.action_queue.extend(results)

    def move_enemies(self):
        """ Process enemy movement. """
        full_results = []
        for creature in self.cur_level.creatures:
            if creature.ai:
                results = creature.ai.take_turn(
                    target=self.player,
                    sprite_lists=[self.cur_level.dungeon_sprites, self.cur_level.creatures],
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
            self.player.position, self.cur_level.dungeon_sprites
        )
        # For each entity
        for entity in entities:
            if isinstance(entity, Stairs):
                level = self.setup_level(self.cur_level.level + 1)
                self.cur_level = level
                self.levels.append(level)
                return [{"message": "You went down a level."}]

        return [{"message": "There are no stairs here"}]

    def pick_up(self):
        """
        Handle a pick-up item entity request.
        """
        # Get all the entities at this location
        entities = arcade.get_sprites_at_exact_point(
            self.player.position, self.cur_level.entities
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

    def check_experience_level(self):
        """
        See if the player should level up
        """
        if self.player.fighter.level < len(EXPERIENCE_PER_LEVEL):
            xp_to_next_level = EXPERIENCE_PER_LEVEL[self.player.fighter.level - 1]
            if self.player.fighter.current_xp >= xp_to_next_level:
                self.player.fighter.ability_points += 1
                self.player.fighter.level += 1
                self.action_queue.extend([{"message": "Level up!!!"}])
                arcade.play_sound(self.level_up_sound)

    def process_action_queue(self, delta_time: float):
        """
        Process the action queue, kind of a dispatch-center for the game.
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
                arcade.play_sound(self.monster_death)
                if new_actions:
                    new_action_queue.extend(new_actions)
            if "dead" in action:
                target = action["dead"]
                target.texture_id = DEAD_BODY_TEXTURE_ID
                target.color = colors["dead_body"]
                target.visible_color = colors["dead_body"]
                target.blocks = False
                if target is not self.player:
                    self.player.fighter.current_xp += target.fighter.xp_reward

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

            if "play_sound" in action:
                target = action["play_sound"]
                if target == "monster_walk":
                    arcade.play_sound(self.monster_walk_sound)
                elif target == "monster_attack":
                    arcade.play_sound(self.monster_attack_sound)
                elif target == "pickup_potion":
                    arcade.play_sound(self.pickup_potion_sound)
                elif target == "pickup_scroll":
                    arcade.play_sound(self.pickup_scroll_sound)
                elif target == "heal":
                    arcade.play_sound(self.heal_sound)
                elif target == "error":
                    arcade.play_sound(self.error_sound)
                else:
                    print(f"Warning, unknown sound trigger {target}.")

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
