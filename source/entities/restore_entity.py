from entities.potion import Potion
from entities.fireball_scroll import FireballScroll
from entities.stairs import Stairs
from entities.lightning_scroll import LightningScroll
from entities.entity import Entity


def restore_entity(entity_dict):
    entity_name = list(entity_dict.keys())[0]

    if entity_name == 'Entity':
        entity = Entity()
    elif entity_name == 'Potion':
        entity = Potion()
    elif entity_name == 'FireballScroll':
        entity = FireballScroll()
    elif entity_name == 'LightningScroll':
        entity = LightningScroll()
    elif entity_name == 'Stairs':
        entity = Stairs()
    else:
        raise ValueError(f"Error, don't know how to restore {entity_name}.")

    entity.restore_from_dict(entity_dict[entity_name])

    return entity
