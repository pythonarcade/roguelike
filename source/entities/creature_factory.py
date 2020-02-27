import random
import csv

def load_creatures(filename):
    monsters = []
    with open(filename) as input_file:
        reader = csv.DictReader(input_file, delimiter='\t')
        for creature in reader:
            monsters.append(creature)

    return monsters


monsters = load_creatures("creatures.tsv")

def convert_to_restore_dict(monster):
    converted = {}
    converted['texture'] = int(monster['Texture'])
    converted['name'] = monster['Name']
    converted['fighter'] = {
                "defense": int(monster['Defense']),
                "hp": int(monster['HP']),
                "max_hp": int(monster['HP']),
                "power": int(monster['Attack']),
                "xp_reward": int(monster['XP']),
            },
    return converted

def get_random_monster_by_challenge(challenge):
    filtered_monsters = [monster for monster in monsters if int(monster['Challenge']) == challenge]
    m1 = random.choice(filtered_monsters)
    m2 = convert_to_restore_dict(m1)
    return m2

m = get_random_monster_by_challenge(1)
print(m)