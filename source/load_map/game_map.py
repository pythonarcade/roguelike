from constants import TILE
from entities.entity import Entity
from load_map.dungeon_map import DungeonMap


class GameMap:
    def __init__(self, level_number: int = 1):
        self.map_width = 0
        self.map_height = 0
        self.dungeon_map: DungeonMap = DungeonMap()
        self.level_number = level_number

        self.tiles = [
            [TILE.WALL for _ in range(self.map_height)] for _ in range(self.map_width)
        ]
        self.entities = [
            [TILE.EMPTY for _ in range(self.map_height)] for _ in range(self.map_width)
        ]
        self.creatures = [
            [TILE.EMPTY for _ in range(self.map_height)] for _ in range(self.map_width)
        ]

    def make_map(
        self, player: Entity, level: int
    ):
        self.dungeon_map.load(f"levels/level_{level:02}.json")
        self.map_width = self.dungeon_map.map_width
        self.map_height = self.dungeon_map.map_height

        self.tiles = []
        for row in range(self.map_height):
            self.tiles.append([])
            for column in range(self.map_width):
                tile = self.dungeon_map.tiles[row][column]
                if tile.cell == 0 or tile.perimeter:
                    self.tiles[row].append(TILE.WALL)
                elif tile.corridor:
                    self.tiles[row].append(TILE.FLOOR)
                elif tile.room:
                    self.tiles[row].append(TILE.FLOOR)
                else:
                    self.tiles[row].append(TILE.EMPTY)

        player.x = 10
        player.y = 11

        # self.tiles = [
        #     [TILE.WALL for _ in range(self.map_height)] for _ in range(self.map_width)
        # ]
        self.entities = [
            [TILE.EMPTY for _ in range(self.map_height)] for _ in range(self.map_width)
        ]
        self.creatures = [
            [TILE.EMPTY for _ in range(self.map_height)] for _ in range(self.map_width)
        ]
