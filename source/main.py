"""
Starting Template Simple

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template_simple
"""
import arcade
import pyglet.gl as gl
import math

from game_map import GameMap

SCREEN_TITLE = "RogueLike"
SCALE = 1
SPRITE_WIDTH = 9
SPRITE_HEIGHT = 16
ROWS = 60
COLUMNS = 150
SCREEN_WIDTH = SPRITE_WIDTH * COLUMNS
SCREEN_HEIGHT = SPRITE_HEIGHT * ROWS
WALL_CHAR = 219
FOV_RADIUS = 10

colors = {
    'dark_wall': (0, 0, 100),
    'dark_ground': (50, 50, 150),
    'light_wall': (130, 110, 50),
    'light_ground': (200, 180, 50)
}

textures = arcade.load_spritesheet(":resources:images/spritesheets/codepage_437.png",
                                   sprite_width=SPRITE_WIDTH,
                                   sprite_height=SPRITE_HEIGHT,
                                   columns=32,
                                   count=8 * 32)

class Item(arcade.Sprite):
    """ Character Sprite on Screen """
    def __init__(self, letter, color):
        super().__init__(scale=SCALE)
        self._x = 0
        self._y = 0
        self.color = color
        self.char = letter
        self.block_sight = False
        self.is_visible = False

    @property
    def char(self):
        """ Character of the item """
        return self._char

    @char.setter
    def char(self, value):
        self._char = value
        self.texture = textures[self._char]

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.center_x = self._x * SPRITE_WIDTH * SCALE + SPRITE_WIDTH / 2 * SCALE

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.center_y = self._y * SPRITE_HEIGHT * SCALE + SPRITE_HEIGHT / 2 * SCALE

def char_to_pixel(char_x, char_y):
    px = char_x * SPRITE_WIDTH * SCALE + SPRITE_WIDTH / 2 * SCALE
    py = char_y * SPRITE_HEIGHT * SCALE + SPRITE_HEIGHT / 2 * SCALE
    return px, py

def recalculate_fov(char_x, char_y, radius, sprite_list):
    for sprite in sprite_list:
        sprite.is_visible = False

    circumference = 2 * math.pi * radius
    print(circumference)

    radians_per_point = 2 * math.pi / circumference
    for i in range(int(round(circumference))):
        radians = i * radians_per_point

        x = math.sin(radians) * radius + char_x
        y = math.cos(radians) * radius + char_y

        for j in range(radius):
            v1 = char_x, char_y
            v2 = x, y
            x2, y2 = arcade.lerp_vec(v1, v2, j/radius)

            pixel_point = char_to_pixel(x2, y2)

            sprites_at_point = arcade.get_sprites_at_point(pixel_point, sprite_list)
            blocked = False
            for sprite in sprites_at_point:
                sprite.is_visible = True
                if sprite.block_sight:
                    blocked = True
            if blocked:
                break


    for sprite in sprite_list:
        if sprite.is_visible and sprite.block_sight:
            sprite.color = colors['light_wall']
        elif not sprite.is_visible and sprite.block_sight:
            sprite.color = colors['dark_wall']
        elif not sprite.is_visible and not sprite.block_sight:
            sprite.color = colors['dark_ground']
        elif sprite.is_visible and not sprite.block_sight:
            sprite.color = colors['light_ground']



class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title, antialiasing=False)

        arcade.set_background_color(arcade.color.BLACK)
        self.player = None
        self.characters = None
        self.game_map = None
        self.dungeon_sprites = None

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        self.characters = arcade.SpriteList()
        self.dungeon_sprites = arcade.SpriteList(use_spatial_hash=True,
                                                 spatial_hash_cell_size=16)

        self.player = Item(ord("@"), arcade.csscolor.WHITE)
        self.player.x = 0
        self.player.y = 0
        self.characters.append(self.player)

        # Size of the map
        map_width = COLUMNS
        map_height = ROWS

        # Some variables for the rooms in the map
        room_max_size = 10
        room_min_size = 6
        max_rooms = 30

        self.game_map = GameMap(map_width, map_height)
        self.game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, self.player)
        print(self.player.x, self.player.y)

        # Draw all the tiles in the game map
        for y in range(self.game_map.height):
            for x in range(self.game_map.width):
                wall = self.game_map.tiles[x][y].block_sight

                if wall:
                    sprite = Item(WALL_CHAR, colors.get('dark_wall'))
                    sprite.block_sight = True
                else:
                    sprite = Item(WALL_CHAR, colors.get('dark_ground'))
                    sprite.block_sight = False

                sprite.x = x
                sprite.y = y

                self.dungeon_sprites.append(sprite)


    def on_draw(self):
        """
        Render the screen.
        """

        arcade.start_render()

        self.dungeon_sprites.draw(filter=gl.GL_NEAREST)
        self.characters.draw(filter=gl.GL_NEAREST)

    def on_key_press(self, symbol: int, modifiers: int):
        """ Manage keyboard input """
        try:
            player_moved = False
            if symbol == arcade.key.UP:
                self.player.y += 1
                player_moved = True
            elif symbol == arcade.key.DOWN:
                self.player.y -= 1
                player_moved = True
            elif symbol == arcade.key.LEFT:
                self.player.x -= 1
                player_moved = True
            elif symbol == arcade.key.RIGHT:
                self.player.x += 1
                player_moved = True

            if player_moved:
                recalculate_fov(self.player.x, self.player.y, FOV_RADIUS, self.dungeon_sprites)
        except Exception as e:
            print(e)


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
