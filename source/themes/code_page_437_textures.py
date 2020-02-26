import arcade
from themes.current_theme import *

# Load  the textures our sprites use on game start-up.
textures = arcade.load_spritesheet(
    ":resources:images/spritesheets/codepage_437.png",
    sprite_width=SPRITE_WIDTH,
    sprite_height=SPRITE_HEIGHT,
    columns=32,
    count=8 * 32,
)
