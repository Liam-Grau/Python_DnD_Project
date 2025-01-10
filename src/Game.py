from src.Player import *
from src.Map import *
from src.Item import *
import keyboard as kb
from time import sleep


class Game:

    def __init__(self):
        items = list(json.loads(open('data/Items.json').read()).items())
        self.dict_items = {key: [Item(x[0], x[1], x[2], x[3], x[4])
                                 for x in value] for key, value in items}

        attacks = list(json.loads(open('data/Attacks.json').read()).items())
        self.dict_attacks = {key: [Attack(x[0], x[1], x[2], x[3], x[4])
                                   for x in value] for key, value in attacks}

        print('Bien venu noble aventurier dans "Dragon et Donjon"!\n')
        map_dimension = [0, 0]
        map_dimension[0] = int(input('Quelle devrait être la largeur du monde : '))
        map_dimension[1] = int(input('Et pour la longueur : '))
        name = colored_str(
            input('Etre cherchant trésores et avantures, donne moi ton nom : '), Color.GREEN)
        random_skill = bool(
            int(input("Veux tu choisir tes statistiques (0) ou laisseras tu l'univers décider (1): ")))
        self.player = Player(name, 1, random_skill)
        self.player.add_attacks(self.dict_attacks["Character"] + self.dict_attacks["Player"])
        self.map = Map(map_dimension)
        print(self.map)
        self.end = False

    def begin_game(self):
        random_pos = np.random.randint(low=0, high=self.map.dimension[1], size=(2,))
        self.map.set_tile_type(random_pos, TileType.PLAYER)
        self.player.set_pos(random_pos)

    # to do
    def spawn_item(self):
        return

    def spawn_enemy(self):
        return

    def item_interaction(self, item):
        return

    def enemy_interaction(self, enemies):
        return
    # to do

    def check_tile(self):
        print("\n============================================================\n")
        player_pos = self.player.pos
        if self.map.map[player_pos[0]][player_pos[1]].tile_type == TileType.ITEM:
            print("IIITTEEMMM!\n")
            item = self.spawn_item()
            self.item_interaction(item)
        elif self.map.map[player_pos[0]][player_pos[1]].tile_type == TileType.ENEMY:
            print("Baston!\n")
            enemies = self.spawn_enemy()
            self.enemy_interaction(enemies)
        else:
            print("Il n'y a rien à cet endroit... Décevant!\n")

    def game_round(self):
        while(not self.end):
            self.map.set_tile_type(self.player.pos, TileType.PLAYER)
            self.map.draw(self.player.pos)
            print("(w = haut, a = gauche, s = bas, d = droite, q = quit)")
            sleep(0.2)

            key = kb.read_key()
            if key.lower() in {'a', 'd', 'w', 's'}:
                self.map.update(self.player.pos)

                if (key.lower() == 'a'):
                    self.player.pos[1] -= 1

                    if (self.player.pos[1] < 0):
                        self.player.pos[1] = self.map.dimension[1] - 1

                elif (key.lower() == 'd'):
                    self.player.pos[1] += 1

                    if (self.player.pos[1] > self.map.dimension[1] - 1):
                        self.player.pos[1] = 0

                elif (key.lower() == 'w'):
                    self.player.pos[0] -= 1

                    if (self.player.pos[0] < 0):
                        self.player.pos[0] = self.map.dimension[0] - 1

                elif (key.lower() == 's'):
                    self.player.pos[0] += 1

                    if (self.player.pos[0] > self.map.dimension[1] - 1):
                        self.player.pos[0] = 0

                self.check_tile()

            elif (key.lower() == 'q'):
                self.end = True
