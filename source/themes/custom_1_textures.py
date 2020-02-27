import pathlib

from arcade import load_texture
from themes.current_theme import *

assets_path = pathlib.Path(__file__).resolve().parent / "custom_1"

# Load  the textures our sprites use on game start-up.
textures = []

textures.append(load_texture(assets_path / "floor.png"))
textures.append(load_texture(assets_path / "player.png"))
textures.append(load_texture(assets_path / "orc.png"))
textures.append(load_texture(assets_path / "troll.png"))
textures.append(load_texture(assets_path / "wall.png"))
textures.append(load_texture(assets_path / "red_potion.png"))
textures.append(load_texture(assets_path / "scroll.png"))
textures.append(load_texture(assets_path / "dead_body.png"))
textures.append(load_texture(assets_path / "stairs_down.png"))
