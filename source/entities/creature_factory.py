from pathlib import Path
import random
import csv
from themes.current_theme import colors
from entities.entity import Entity
from arcade import load_texture
from entities.ai import BasicMonster
from entities.fighter import Fighter


def load_creatures(monsters_path: Path):
    with open(monsters_path) as input_file:
        reader = csv.DictReader(input_file, delimiter='\t')
        return [creature for creature in reader]


monsters_path = Path(__file__).resolve().parent / "creatures.tsv"
monsters = load_creatures(monsters_path)


def get_random_monster_by_challenge(challenge):
    filtered_monsters = [monster for monster in monsters if int(monster['Challenge']) == challenge]
    if len(filtered_monsters) == 0:
        raise ValueError(f"Error, no creatures for challenge level {challenge}.")
    m1 = random.choice(filtered_monsters)
    return m1


def make_monster_sprite(monster_dict):
    sprite = Entity()
    sprite.texture = load_texture(monster_dict['Texture'])
    sprite.ai = BasicMonster()
    sprite.ai.owner = sprite
    sprite.fighter = Fighter()
    sprite.fighter.owner = sprite
    sprite.fighter.hp = int(monster_dict['HP'])
    sprite.fighter.power = int(monster_dict['Attack'])
    sprite.fighter.defense = int(monster_dict['Defense'])
    sprite.fighter.xp_reward = int(monster_dict['XP'])
    sprite.not_visible_color = colors['transparent']
    sprite.blocks = True
    sprite.name = monster_dict['Name']
    return sprite

# m = get_random_monster_by_challenge(1)
# print(m)
# e = make_monster_sprite(m)
