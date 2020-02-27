import random
import csv
from entities.entity import Entity
from arcade import load_texture
from entities.ai import BasicMonster
from entities.fighter import Fighter


def load_creatures(filename):
    monsters = []
    with open(filename) as input_file:
        reader = csv.DictReader(input_file, delimiter='\t')
        for creature in reader:
            monsters.append(creature)

    return monsters


monsters = load_creatures("entities/creatures.tsv")

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
    sprite.blocks = True
    sprite.name = monster_dict['Name']
    print(f"Made a {sprite.name}.")
    return sprite

# m = get_random_monster_by_challenge(1)
# print(m)
# e = make_monster_sprite(m)