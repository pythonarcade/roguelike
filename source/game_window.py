"""
Main Game Engine
"""
import arcade
import pyglet.gl as gl

from constants import *
from entity import Entity
from status_bar import draw_status_bar
from game_engine import GameEngine
from util import pixel_to_char
from util import char_to_pixel


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
        self.mouse_position = None

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        self.game_engine.setup()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.game_engine.game_state == SELECT_LOCATION:
            grid_x, grid_y = pixel_to_char(x, y)
            self.game_engine.grid_click(grid_x, grid_y)
        self.game_engine.game_state = NORMAL

    def on_draw(self):
        """
        Render the screen.
        """
        try:
            arcade.start_render()

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

            if self.game_engine.game_state == NORMAL:
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
                    text = f"{i+1}: {item_name}"
                    arcade.draw_text(text, x, y, colors["status_panel_text"])

                # Check message queue. Limit to 2 lines
                while len(self.game_engine.messages) > 2:
                    self.game_engine.messages.pop(0)

                # Draw messages
                y = 20
                for message in self.game_engine.messages:
                    arcade.draw_text(message, 200, y, colors["status_panel_text"])
                    y -= 20

                # Draw mouse-over text
                if self.mouse_over_text:
                    x, y = self.mouse_position
                    arcade.draw_xywh_rectangle_filled(x, y, 100, 16, arcade.color.BLACK)
                    arcade.draw_text(self.mouse_over_text, x, y, arcade.csscolor.WHITE)

            elif self.game_engine.game_state == SELECT_LOCATION:
                mouse_x, mouse_y = self.mouse_position
                grid_x, grid_y = pixel_to_char(mouse_x, mouse_y)
                center_x, center_y = char_to_pixel(grid_x, grid_y)
                arcade.draw_rectangle_outline(center_x, center_y, SPRITE_WIDTH, SPRITE_HEIGHT, arcade.color.LIGHT_BLUE, 2)

        except Exception as e:
            print(e)

    def on_key_press(self, key: int, modifiers: int):
        """ Manage keyboard input """
        self.time_since_last_move_check = None
        if key in KEYMAP_UP:
            self.up_pressed = True
        elif key == arcade.key.SPACE:
            self.game_engine.game_state = SELECT_LOCATION
        elif key == arcade.key.ESCAPE:
            self.game_engine.game_state = NORMAL
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
        elif key in KEYMAP_PICKUP:
            self.game_engine.action_queue.extend([{"pickup": True}])
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
        elif key in KEYMAP_DROP_ITEM:
            self.game_engine.action_queue.extend([{"drop_item": True}])

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
        self.mouse_position = x, y
        sprite_list = arcade.get_sprites_at_point((x, y), self.game_engine.entities)
        self.mouse_over_text = None
        for sprite in sprite_list:
            if isinstance(sprite, Entity):
                if sprite.fighter and sprite.is_visible:
                    self.mouse_over_text = (
                        f"{sprite.name} {sprite.fighter.hp}/{sprite.fighter.max_hp}"
                    )
            else:
                raise TypeError("Sprite is not an instance of Entity class.")

    def check_for_player_movement(self):
        if self.game_engine.player.is_dead:
            return

        self.time_since_last_move_check = 0
        cx = 0
        cy = 0

        if self.up_pressed or self.up_left_pressed or self.up_right_pressed:
            cy += 1
        if self.down_pressed or self.down_left_pressed or self.down_right_pressed:
            cy -= 1

        if self.left_pressed or self.down_left_pressed or self.up_left_pressed:
            cx -= 1
        if self.right_pressed or self.down_right_pressed or self.up_right_pressed:
            cx += 1

        if cx or cy:
            self.game_engine.move_player(cx, cy)

    def on_update(self, delta_time: float):

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

        self.game_engine.process_action_queue(delta_time)


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
