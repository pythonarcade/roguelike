"""
Main Game Engine
"""
from typing import Optional, Tuple

import arcade
import json
import pyglet.gl as gl

from constants import *
from entities.entity import Entity
from status_bar import draw_status_bar
from game_engine import GameEngine
from util import pixel_to_char
from util import char_to_pixel
from themes.current_theme import *


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width: int, height: int, title: str):
        super().__init__(width, height, title, antialiasing=False)

        self.game_engine = GameEngine()

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.up_left_pressed = False
        self.up_right_pressed = False
        self.down_left_pressed = False
        self.down_right_pressed = False

        self.time_since_last_move_check = 0

        self.mouse_over_text = None
        self.mouse_position: Optional[Tuple[float, float]] = None

        print("Background, ", colors['background'])
        arcade.set_background_color(colors['background'])

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        self.game_engine.setup()

    def draw_hp_and_status_bar(self):
        text = f"HP: {self.game_engine.player.fighter.hp}/{self.game_engine.player.fighter.max_hp}"
        arcade.draw_text(text, 0, 0, colors["status_panel_text"])
        size = 65
        margin = 2
        draw_status_bar(
            size / 2 + margin,
            24,
            size,
            10,
            self.game_engine.player.fighter.hp,
            self.game_engine.player.fighter.max_hp,
        )

    def draw_inventory(self):
        capacity = self.game_engine.player.inventory.capacity
        selected_item = self.game_engine.selected_item

        field_width = SCREEN_WIDTH / (capacity + 1)
        for i in range(capacity):
            y = 40
            x = i * field_width
            if i == selected_item:
                arcade.draw_lrtb_rectangle_outline(
                    x - 1, x + field_width - 5, y + 20, y, arcade.color.BLACK, 2
                )
            if self.game_engine.player.inventory.items[i]:
                item_name = self.game_engine.player.inventory.items[i].name
            else:
                item_name = ""
            text = f"{i + 1}: {item_name}"
            arcade.draw_text(text, x, y, colors["status_panel_text"])

    def draw_mouse_over_text(self):
        if self.mouse_over_text:
            x, y = self.mouse_position
            arcade.draw_xywh_rectangle_filled(x, y, 100, 16, arcade.color.BLACK)
            arcade.draw_text(self.mouse_over_text, x, y, arcade.csscolor.WHITE)

    def draw_in_normal_state(self):
        self.draw_hp_and_status_bar()
        self.draw_inventory()
        self.handle_and_draw_messages()
        self.draw_mouse_over_text()

    def draw_in_select_location_state(self):
        mouse_x, mouse_y = self.mouse_position
        grid_x, grid_y = pixel_to_char(mouse_x, mouse_y)
        center_x, center_y = char_to_pixel(grid_x, grid_y)
        arcade.draw_rectangle_outline(
            center_x,
            center_y,
            SPRITE_WIDTH,
            SPRITE_HEIGHT,
            arcade.color.LIGHT_BLUE,
            2,
        )

    def handle_and_draw_messages(self):
        # Check message queue. Limit to 2 lines
        while len(self.game_engine.messages) > 2:
            self.game_engine.messages.pop(0)

        # Draw messages
        y = 20
        for message in self.game_engine.messages:
            arcade.draw_text(message, 200, y, colors["status_panel_text"])
            y -= 20

    def draw_sprites_and_status_panel(self):
        # Draw the sprites
        self.game_engine.dungeon_sprites.draw(filter=gl.GL_NEAREST)
        self.game_engine.entities.draw(filter=gl.GL_NEAREST)
        self.game_engine.characters.draw(filter=gl.GL_NEAREST)

        # Draw the status panel
        arcade.draw_xywh_rectangle_filled(
            0,
            0,
            SCREEN_WIDTH,
            STATUS_PANEL_HEIGHT,
            colors["status_panel_background"],
        )

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """
        Handle mouse-down events
        """
        # If we are currently in a 'select location' state, process
        if self.game_engine.game_state == SELECT_LOCATION:
            # Grab grid location
            grid_x, grid_y = pixel_to_char(x, y)
            # Notify game engine
            self.game_engine.grid_click(grid_x, grid_y)

    def on_draw(self):
        """
        Render the screen.
        """
        try:
            arcade.start_render()

            self.draw_sprites_and_status_panel()

            if self.game_engine.game_state == NORMAL:
                self.draw_in_normal_state()
            elif self.game_engine.game_state == SELECT_LOCATION:
                self.draw_in_select_location_state()

        except Exception as e:
            print("Draw exception:", e)

    def on_key_press(self, key: int, modifiers: int):
        """ Manage key-down events """

        # Clear the timer for auto-repeat of movement
        self.time_since_last_move_check = None

        if key in KEYMAP_UP:
            self.up_pressed = True
        elif key == arcade.key.SPACE:
            self.game_engine.game_state = SELECT_LOCATION
        elif key == arcade.key.ESCAPE:
            self.game_engine.game_state = NORMAL

        # Movement
        elif key in KEYMAP_DOWN:
            self.down_pressed = True
        elif key in KEYMAP_LEFT:
            self.left_pressed = True
        elif key in KEYMAP_RIGHT:
            self.right_pressed = True
        elif key in KEYMAP_UP_LEFT:
            self.up_left_pressed = True
        elif key in KEYMAP_UP_RIGHT:
            self.up_right_pressed = True
        elif key in KEYMAP_DOWN_LEFT:
            self.down_left_pressed = True
        elif key in KEYMAP_DOWN_RIGHT:
            self.down_right_pressed = True

        # Item management
        elif key in KEYMAP_PICKUP:
            self.game_engine.action_queue.extend([{"pickup": True}])
        elif key in KEYMAP_DROP_ITEM:
            self.game_engine.action_queue.extend([{"drop_item": True}])
        elif key in KEYMAP_SELECT_ITEM_1:
            self.game_engine.action_queue.extend([{"select_item": 1}])
        elif key in KEYMAP_SELECT_ITEM_2:
            self.game_engine.action_queue.extend([{"select_item": 2}])
        elif key in KEYMAP_SELECT_ITEM_3:
            self.game_engine.action_queue.extend([{"select_item": 3}])
        elif key in KEYMAP_SELECT_ITEM_4:
            self.game_engine.action_queue.extend([{"select_item": 4}])
        elif key in KEYMAP_SELECT_ITEM_5:
            self.game_engine.action_queue.extend([{"select_item": 5}])
        elif key in KEYMAP_SELECT_ITEM_6:
            self.game_engine.action_queue.extend([{"select_item": 6}])
        elif key in KEYMAP_SELECT_ITEM_7:
            self.game_engine.action_queue.extend([{"select_item": 7}])
        elif key in KEYMAP_SELECT_ITEM_8:
            self.game_engine.action_queue.extend([{"select_item": 8}])
        elif key in KEYMAP_SELECT_ITEM_9:
            self.game_engine.action_queue.extend([{"select_item": 9}])
        elif key in KEYMAP_SELECT_ITEM_0:
            self.game_engine.action_queue.extend([{"select_item": 0}])
        elif key in KEYMAP_USE_ITEM:
            self.game_engine.action_queue.extend([{"use_item": True}])

        # Save/load
        elif key == arcade.key.S:
            self.save()
        elif key == arcade.key.L:
            self.load()

        elif key in KEYMAP_USE_STAIRS:
            self.game_engine.action_queue.extend([{"use_stairs": True}])

    def on_key_release(self, key: int, modifiers: int):
        """Called when the user releases a key. """

        if key in KEYMAP_UP:
            self.up_pressed = False
        elif key in KEYMAP_DOWN:
            self.down_pressed = False
        elif key in KEYMAP_LEFT:
            self.left_pressed = False
        elif key in KEYMAP_RIGHT:
            self.right_pressed = False
        elif key in KEYMAP_UP_LEFT:
            self.up_left_pressed = False
        elif key in KEYMAP_UP_RIGHT:
            self.up_right_pressed = False
        elif key in KEYMAP_DOWN_LEFT:
            self.down_left_pressed = False
        elif key in KEYMAP_DOWN_RIGHT:
            self.down_right_pressed = False

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ Handle mouse motion, mostly just used for mouse-over text. """

        # Get current mouse position. Used elsewhere when we need it.
        self.mouse_position = x, y

        # Get the sprites at the current location
        sprite_list = arcade.get_sprites_at_point((x, y), self.game_engine.entities)

        # See if any sprite we are hovering over deserves a mouse-over text
        self.mouse_over_text = None
        for sprite in sprite_list:
            if isinstance(sprite, Entity):
                if sprite.fighter and sprite.is_visible:
                    self.mouse_over_text = (
                        f"{sprite.name} {sprite.fighter.hp}/{sprite.fighter.max_hp}"
                    )
            else:
                raise TypeError("Sprite is not an instance of Entity class.")

    def save(self):
        """ Save the current game to disk. """
        game_dict = self.game_engine.get_dict()

        with open("game_save.json", "w") as write_file:
            json.dump(game_dict, write_file, indent=4, sort_keys=True)

        results = [{"message": "Game has been saved"}]
        self.game_engine.action_queue.extend(results)

    def load(self):
        """ Load the game from disk. """
        with open("game_save.json", "r") as read_file:
            data = json.load(read_file)

        self.game_engine.restore_from_dict(data)

    def check_for_player_movement(self):
        """
        Figure out if we should move the player or not based on keys currently
        held down.
        """

        # Player is dead, don't move her.
        if self.game_engine.player.is_dead:
            return

        # Reset the movement clock used for holding the key down for repeated movement.
        self.time_since_last_move_check = 0

        # cx and cy are the delta in movement. Start with no movement.
        cx = 0
        cy = 0

        # Adjust delta of movement based on keys pressed
        if self.up_pressed or self.up_left_pressed or self.up_right_pressed:
            cy += 1
        if self.down_pressed or self.down_left_pressed or self.down_right_pressed:
            cy -= 1

        if self.left_pressed or self.down_left_pressed or self.up_left_pressed:
            cx -= 1
        if self.right_pressed or self.down_right_pressed or self.up_right_pressed:
            cx += 1

        # If we are trying to move, pass that request to the game_engine
        if cx or cy:
            self.game_engine.move_player(cx, cy)

    def on_update(self, delta_time: float):
        """ Manage regular updates for the game """

        # --- Manage continuous movement while direction keys are held down

        # Time since last check, if we are tracking
        if self.time_since_last_move_check is not None:
            self.time_since_last_move_check += delta_time

        # Check if we should move again based on the clock, or if the clock
        # was set to None as a trigger to move immediate
        if (
            self.time_since_last_move_check is None
            or self.time_since_last_move_check >= REPEAT_MOVEMENT_DELAY
        ):
            self.check_for_player_movement()

        # --- Process the action queue
        self.game_engine.process_action_queue(delta_time)


def main():
    """ Main method for starting the rogue-like game """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
