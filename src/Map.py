import numpy as np
from functools import reduce
import random
from src.Color import *
import json


class TileType(Enum):
    NONE = 0
    ENEMY = 1
    ITEM = 2
    TREASURE = 3

class TileBiome(Enum):
    NONE = "BLACK"
    WATER = "LIGHT_BLUE"
    SAND = "YELLOW"
    GRASSLAND = "LIGHT_GREEN"
    HILL = "DARK_GREEN"
    MOUNTAIN = "GRAY"
    VOLCANO = "RED"

class Tile:

    def __init__(self, tile_type=TileType.NONE, biome=TileBiome.NONE, discovered=False, player = False):
        self.tile_type = tile_type
        self.biome = biome
        self.discovered = discovered
        self.player = player

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
    
    @property
    def __dict__(self):
        return {"tile_type": self.tile_type.name, "biome" : self.biome.name, "discovered": self.discovered, "player": self.player}


class Map:

    def choose_tile_tipe(self, num=0.0):
        if (num > self.item_spawn_chance):
            return Tile(TileType.NONE)
        elif (num > self.mob_spawn_chance):
            return Tile(TileType.ITEM)
        else:
            return Tile(TileType.ENEMY)

    def __init__(self, dimension=[10, 10], mob_spawn_chance=0.45, item_spawn_chance=0.65, nothing_spawn_chance=1.0):
        self.markov_chain = dict(json.loads(open('data/Biome.json').read()))
        self.dimension = dimension
        self.mob_spawn_chance = mob_spawn_chance
        self.item_spawn_chance = item_spawn_chance
        self.nothing_spawn_chance = nothing_spawn_chance

        self.map = []

        self.discovered_tiles = set()

    def save(self):
        saved_map = vars(self)
        tiles = list(map(lambda row : list(map(lambda tile : tile.__dict__, row)), saved_map["map"]))
        saved_map["map"] = tiles
        discovered_tiles = list(map(lambda tile: tile.__dict__, saved_map["discovered_tiles"]))
        saved_map["discovered_tiles"] = discovered_tiles
        with open("data/saved_map.json", "w") as file:
            json.dump(saved_map, file, indent = 4)

    def get_saved_map(self):
        try:
            with open("data/saved_map.json", "r") as file:
                saved_map = json.load(file)
            self.dimension = saved_map.get("dimension", [10, 10])
            self.mob_spawn_chance = saved_map.get("mob_spawn_chance", 0.45)
            self.item_spawn_chance = saved_map.get("item_spawn_chance", 0.65)
            self.nothing_spawn_chance = saved_map.get("nothing_spawn_chance", 1)
            
            new_map = np.empty((self.dimension[0], self.dimension[1]), dtype = Tile)

            for i in range(self.dimension[0]): 
                for j in range(self.dimension[1]): 
                    tile = saved_map["map"][i][j]
                    new_map[i][j] = Tile(TileType[tile["tile_type"]], TileBiome[tile["biome"]], tile["discovered"], tile["player"])

            self.map = new_map

            discovered_tiles = set()
            for i in range(len(saved_map["discovered_tiles"])):
                tile = saved_map["discovered_tiles"][i]
                discovered_tiles.add(Tile(TileType[tile["tile_type"]], TileBiome[tile["biome"]], tile["discovered"], tile["player"]))

            self.discovered_tiles = discovered_tiles
        except FileNotFoundError:
            raise

    def delete_save(self):
        os.remove("data/saved_map.json")

    def initialize_biome(self, tile, pos):
        around_tile = [self.map[self.dimension[0] - 1 if pos[0] - 1 < 0 else pos[0] - 1][self.dimension[1] - 1 if pos[1] - 1 < 0 else pos[1] - 1],
                       self.map[self.dimension[0] - 1 if pos[0] - 1 < 0 else pos[0] - 1][pos[1]],
                       self.map[self.dimension[0] - 1 if pos[0] - 1 < 0 else pos[0] - 1][(pos[1] + 1) % self.dimension[1]],
                       self.map[pos[0]][self.dimension[1] - 1 if pos[1] - 1 < 0 else pos[1] - 1],
                       self.map[pos[0]][(pos[1] + 1) % self.dimension[1]],
                       self.map[(pos[0] + 1) % self.dimension[0]][self.dimension[1] - 1 if pos[1] - 1 < 0 else pos[1] - 1],
                       self.map[(pos[0] + 1) % self.dimension[0]][pos[1]],
                       self.map[(pos[0] + 1) % self.dimension[0]][(pos[1] + 1) % self.dimension[1]]]
        
        average_markov_chain = {biome.name: reduce(lambda x, tile: x + self.markov_chain[tile.biome.name][biome.name], around_tile, 0) for biome in TileBiome if biome != TileBiome.NONE}
        average_markov_chain = {biome: value / 8 for biome, value in average_markov_chain.items()}
        
        max_roll_result = reduce(lambda x, y: x + y, average_markov_chain.values(), 0)
        roll = random.uniform(0.0, max_roll_result)

        for key in average_markov_chain.keys():
            max_roll_result -= average_markov_chain[key]
            if (roll > max_roll_result):
                tile.biome = TileBiome[key]
                return
    
    def initialize_map(self):
         random_map = np.random.uniform(low=0.0, high=self.mob_spawn_chance + self.item_spawn_chance + self.nothing_spawn_chance, size=(self.dimension[0], self.dimension[1]))
         self.map = list(map(lambda row: list(map(self.choose_tile_tipe, row)), random_map))
         [[self.initialize_biome(self.map[r][c], [r, c]) for c in range(self.dimension[1])] for r in range(self.dimension[0])]

    def s_width(self, width):

        try:
            value = int(width)
        except ValueError:
            return False

        if value < 2:
            return False

        self.dimension = [value, self.dimension[1]]
        return True

    def s_height(self, height):

        try:
            value = int(height)
        except ValueError:
            return False

        value = int(height)
        
        if value < 2:
            return

        self.dimension = [self.dimension[0], value]
        return True

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
                    result += colored_str(f"{BackgroundColor[tile.biome.value].value}\u263A", Color.PURPLE)
                elif not tile.discovered:
                    result += f"{BackgroundColor[tile.biome.value].value}" + u"\u25A1" + f"{Color.RESET.value}"
                else:
                    if (tile.tile_type == TileType.NONE):
                        result += colored_str(f'{BackgroundColor[tile.biome.value].value}0')
                    elif (tile.tile_type == TileType.ITEM):
                        result += colored_str(f'{BackgroundColor[tile.biome.value].value}I', Color.DARK_BLUE)
                    else:
                        result += colored_str(f'{BackgroundColor[tile.biome.value].value}M', Color.BLACK)

            result += '\n'

        print(result)

    def set_tile_type(self, pos, tile_type: TileType = TileType.NONE):
        self.map[int(pos[0])][int(pos[1])].tile_type = tile_type

    def player_on_tile(self, pos, var = True):
        self.map[int(pos[0])][int(pos[1])].player = var

    def set_treasure_tile(self, player_pos):
        pos = player_pos

        while pos[0] == player_pos[0] and pos[1] == player_pos[1]:
            pos = [random.randint(0, self.dimension[0] - 1), random.randint(0, self.dimension[1] - 1)]

        self.set_tile_type(pos, TileType.TREASURE)
        self.map[pos[0]][pos[1]].discovered = False
