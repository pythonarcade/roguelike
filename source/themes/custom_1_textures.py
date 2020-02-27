import pathlib

from arcade import load_texture
from themes.current_theme import *

assets_path = pathlib.Path(__file__).resolve().parent / "custom_1"

filenames = [
    "floor.png",
    "player.png",
    "orc.png",
    "troll.png",
    "wall.png",
    "red_potion.png",
    "scroll.png",
    "dead_body.png",
    "stairs_down.png",
]

# Load  the textures our sprites use on game start-up.
textures = [load_texture(str(assets_path / filename)) for filename in filenames]
