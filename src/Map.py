import numpy as np
import random
from src.Color import *
import json


class TileType(Enum):
    NONE = 0
    ENEMY = 1
    ITEM = 2
    TREASURE = 3


class Tile:

    def __init__(self, tile_type=TileType.NONE, discovered=False):
        self.tile_type = tile_type
        self.discovered = discovered
        self.player = False

    def update(self, mob_spawn_chance, item_spawn_chance):
        if (self.discovered and self.tile_type == TileType.NONE and np.random.uniform(low=0.0, high=1.0, size=1) < 0.1):
            self.discovered = False

            num = random.uniform(0.0, 1.0)
            if (num > item_spawn_chance):
                self.tile_type = TileType.NONE
            elif (num > mob_spawn_chance):
                self.tile_type = TileType.ITEM
            else:
                self.tile_type = TileType.ENEMY

        return not self.discovered


class Map:

    def choose_tile_tipe(self, num=0.0):
        if (num > self.item_spawn_chance):
            return Tile(TileType.NONE)
        elif (num > self.mob_spawn_chance):
            return Tile(TileType.ITEM)
        else:
            return Tile(TileType.ENEMY)

    def __init__(self, dimension=[10, 10], mob_spawn_chance=0.45, item_spawn_chance=0.65, nothing_spawn_chance=1.0):
        self.dimension = dimension
        self.mob_spawn_chance = mob_spawn_chance
        self.item_spawn_chance = item_spawn_chance
        self.nothing_spawn_chance = nothing_spawn_chance

        random_map = np.random.uniform(
            low=0.0, high=mob_spawn_chance + item_spawn_chance + nothing_spawn_chance, size=(dimension[0], dimension[1]))
        self.map = list(map(lambda row: list(map(self.choose_tile_tipe, row)), random_map))

        self.discovered_tiles = set()

    def __str__(self):
        result = "Current map :\n"

        for row in self.map:
            for tile in row:
                if (tile.tile_type == TileType.NONE):
                    result += colored_str(' 0')
                elif (tile.tile_type == TileType.ITEM):
                    result += colored_str(' I', Color.GREEN)
                elif tile.tile_type == TileType.ENEMY:
                    result += colored_str(' M', Color.RED)
                else:
                    result += colored_str(' T', Color.YELLOW)

            result += '\n'

        return result

    def update(self, player_pos):
        cur_tile = self.map[int(player_pos[0])][int(player_pos[1])]
        cur_tile.discovered = True
        reset_tile = set()

        for tile in self.discovered_tiles:
            if(tile.update(self.mob_spawn_chance, self.item_spawn_chance)):
                reset_tile.add(tile)
        self.discovered_tiles -= reset_tile
        self.discovered_tiles.add(cur_tile)

    def draw(self, player_pos):
        result = "Your Map :\n"

        for row in self.map:
            for tile in row:
                if tile.player:
                    result += ' ' + colored_str("\u263A", Color.PURPLE)
                elif not tile.discovered:
                    result += ' ' + u"\u25A1"
                else:
                    if (tile.tile_type == TileType.NONE):
                        result += colored_str(' 0')
                    elif (tile.tile_type == TileType.ITEM):
                        result += colored_str(' I', Color.GREEN)
                    else:
                        result += colored_str(' M', Color.RED)

            result += '\n'

        print(result)

    def set_tile_type(self, pos, tile_type: TileType = TileType.NONE):
        self.map[int(pos[0])][int(pos[1])].tile_type = tile_type

    def player_on_tile(self, pos, var = True):
        self.map[int(pos[0])][int(pos[1])].player = var

    def set_treasure_tile(self, player_pos):
        pos = player_pos

        while pos[0] == player_pos[0] and pos[1] == player_pos[1]:
            pos = np.random.randint(low=0, high=self.dimension[1], size=(2,))

        self.set_tile_type(pos, TileType.TREASURE)
