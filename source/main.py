"""
Starting Template Simple

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template_simple
"""
import arcade
import pyglet.gl as gl

from game_map import GameMap
from constants import *
from entity import Entity
from recalculate_fov import recalculate_fov
from util import char_to_pixel


def is_open(x, y, sprite_list):
    px, py = char_to_pixel(x, y)
    sprites = arcade.get_sprites_at_exact_point((px, py), sprite_list)
    for sprite in sprites:
        if sprite.blocks:
            return False
    return True


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title, antialiasing=False)

        arcade.set_background_color(arcade.color.BLACK)
        self.game_map = None
        self.player = None

        self.characters = None
        self.entities = None
        self.dungeon_sprites = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.keyboard_frame_counter = 0

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        self.characters = arcade.SpriteList()
        self.dungeon_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=16
        )
        self.entities = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=16
        )

        self.player = Entity(0, 0, "@", arcade.csscolor.WHITE)
        self.characters.append(self.player)

        # Size of the map
        map_width = MAP_WIDTH
        map_height = MAP_HEIGHT

        # Some variables for the rooms in the map
        room_max_size = 10
        room_min_size = 6
        max_rooms = 30

        self.game_map = GameMap(map_width, map_height)
        self.game_map.make_map(
            max_rooms=max_rooms,
            room_min_size=room_min_size,
            room_max_size=room_max_size,
            map_width=map_width,
            map_height=map_height,
            player=self.player,
            entities=self.entities,
            max_monsters_per_room=3,
        )

        # Draw all the tiles in the game map
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

        recalculate_fov(
            self.player.x,
            self.player.y,
            FOV_RADIUS,
            [self.dungeon_sprites, self.entities],
        )

    def on_draw(self):
        """
        Render the screen.
        """

        arcade.start_render()

        self.dungeon_sprites.draw()
        self.entities.draw()
        self.characters.draw()


    def move(self, cx, cy):
        nx = self.player.x + cx
        ny = self.player.y + cy
        if is_open(nx, ny, self.dungeon_sprites) and is_open(nx, ny, self.entities):
            self.player.x += cx
            self.player.y += cy
            recalculate_fov(
                self.player.x,
                self.player.y,
                FOV_RADIUS,
                [self.dungeon_sprites, self.entities],
            )

    def on_key_press(self, key: int, modifiers: int):
        """ Manage keyboard input """
        if key == arcade.key.UP:
            self.up_pressed = True
            self.keyboard_frame_counter = 0
        elif key == arcade.key.DOWN:
            self.down_pressed = True
            self.keyboard_frame_counter = 0
        elif key == arcade.key.LEFT:
            self.left_pressed = True
            self.keyboard_frame_counter = 0
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
            self.keyboard_frame_counter = 0

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_update(self, dt):
        try:
            cx = 0
            cy = 0
            if self.keyboard_frame_counter % 10 == 0:

                if self.up_pressed and not self.down_pressed:
                    cy = 1
                elif self.down_pressed and not self.up_pressed:
                    cy = -1
                if self.left_pressed and not self.right_pressed:
                    cx = -1
                elif self.right_pressed and not self.left_pressed:
                    cx = 1

                if cx:
                    self.move(cx, 0)
                if cy:
                    self.move(0, cy)

            self.keyboard_frame_counter += 1

        except Exception as e:
            print(e)


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
