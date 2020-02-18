"""
Tile used in creating a procedural dungeon.
Original code from https://github.com/TStand90/roguelike_tutorial_revised
"""


class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """

    def __init__(self, blocks, block_sight=None):
        self.blocks = blocks

        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocks

        self.block_sight = block_sight
