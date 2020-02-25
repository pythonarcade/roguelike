from entities.potion import Potion
from entities.fireball_scroll import FireballScroll
from entities.orc import Orc
from entities.troll import Troll
from entities.lightning_scroll import LightningScroll

def restore_entity(entity_dict):
    entity_name = list(entity_dict.keys())[0]

    if entity_name == 'Potion':
        entity = Potion()
    elif entity_name == 'FireballScroll':
        entity = FireballScroll()
    elif entity_name == 'LightningScroll':
        entity = LightningScroll()
    elif entity_name == 'Orc':
        entity = Orc()
    elif entity_name == 'Troll':
        entity = Troll()
    else:
        raise ValueError(f"Error, don't know how to restore {entity_name}.")

    entity.restore_from_dict(entity_dict[entity_name])

    return entity
