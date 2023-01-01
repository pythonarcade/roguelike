"""
Data objects and JSON loading for dungeon
"""
import json


class Room:
    def __init__(self):
        self.id = 0
        self.room_features = ""


class Tile:
    def __init__(self):
        self.cell = 0
        self.row = 0
        self.column = 0
        self.aperture = 0
        self.arch = 0
        self.block = 0
        self.corridor = 0
        self.door = 0
        self.label = None
        self.locked = 0
        self.perimeter = 0
        self.portcullis = 0
        self.room = 0
        self.room_id = 0
        self.secret = 0
        self.stair_down = 0
        self.stair_up = 0
        self.trapped = 0

    def __str__(self):
        result = f"({self.column}, {self.row}) = {self.cell}"
        if self.room:
            result += "\n  You are in a room."
        if self.room_id:
            result += f"\n  You are in room {self.room_id}."

        return result


class DungeonMap:

    def __init__(self):
        self.cells = {}
        self.bitmask = {}
        self.rooms = {}
        self.map_height = 0
        self.map_width = 0

    def load(self, filename):
        f = open(filename)
        data = json.load(f)
        self.cells = data['cells']
        self.bitmask = data['cell_bit']
        rooms_dict = data['rooms']
        self.rooms = {}
        for room_dict in rooms_dict:
            if room_dict:
                room = Room()
                room.id = room_dict['id']
                if 'detail' in room_dict['contents'] and 'room_features' in room_dict['contents']['detail']:
                    room.room_features = room_dict['contents']['detail']['room_features']
                self.rooms[room.id] = room

        self.map_height = len(self.cells)
        self.tiles = []
        for row_index, row in enumerate(self.cells):
            tile_row = []
            self.tiles.append(tile_row)
            for column_index, cell in enumerate(row):
                tile = Tile()
                tile.cell = cell
                tile.row = row_index
                tile.column = column_index
                tile.aperture = self.get_bitmask_value("aperture", cell)
                tile.arch = self.get_bitmask_value("arch", cell)
                tile.block = self.get_bitmask_value("block", cell)
                tile.corridor = self.get_bitmask_value("corridor", cell)
                tile.door = self.get_bitmask_value("door", cell)
                tile.label = self.get_bitmask_value("label", cell)
                tile.locked = self.get_bitmask_value("locked", cell)
                tile.perimeter = self.get_bitmask_value("perimeter", cell)
                tile.portcullis = self.get_bitmask_value("portcullis", cell)
                tile.room = self.get_bitmask_value("room", cell)
                tile.room_id = self.get_bitmask_value("room_id", cell)
                tile.secret = self.get_bitmask_value("secret", cell)
                tile.stair_down = self.get_bitmask_value("stair_down", cell)
                tile.stair_up = self.get_bitmask_value("stair_up", cell)
                tile.trapped = self.get_bitmask_value("trapped", cell)
                tile_row.append(tile)
        self.map_width = len(self.tiles[0])

    def get_bitmask_value(self, key, cell):
        value = self.bitmask[key] & cell
        temp_mask = self.bitmask[key]
        if not temp_mask:
            return 0
        shift = 0
        while temp_mask >> shift << shift == temp_mask:
            shift += 1
        value2 = value >> (shift - 1)
        return value2

    def get_room(self, id):
        for room_id in self.rooms:
            if self.rooms[room_id] and self.rooms[room_id].id == id:
                return self.rooms[room_id]

    def print_cell(self, cell):
        if not cell:
            print("Nothing")
        for key in self.bitmask:
            value = self.get_bitmask_value(key, cell)
            if value:
                print(f"{key}={value}")