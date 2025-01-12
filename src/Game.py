from numpy import place
from src.Player import *
from src.Enemy import *
from src.Map import *
from src.Item import *
import keyboard as kb
from time import sleep
from functools import reduce
import sys
from src.DialogueEngine import *


class Game:

    def __init__(self):
        items = list(json.loads(open('data/Items.json').read()).items())
        self.dict_items = {key: [Item(x[0], x[1], x[2], x[3], x[4])
                                 for x in value] for key, value in items}

        attacks = list(json.loads(open('data/Attacks.json').read()).items())
        self.dict_attacks = {key: [Attack(x[0], x[1], x[2], x[3], x[4])
                                   for x in value] for key, value in attacks}

        self.map = Map()
        self.player = Player()
        self.player.add_attacks(self.dict_attacks["CHARACTER"] + self.dict_attacks["PLAYER"])

        self.end = False

        self.dialogue_engine = DialogueEngine()
        self.dialogue_engine.load_dialogues("data/Introduction_Dialogue.json")

        # Sets functions callbacks for dialogue system
        funcs = { "s_world_width" : self.map.s_width,
		  "s_world_length" : self.map.s_height,
		  "s_player_name" : self.player.s_name,
		  "choose_stats" : self.player.choose_stats,
		  "rand_stats" : self.player.random_stats,
		  "s_strength" : self.player.s_strength,
		  "s_resistance" : self.player.s_resistance,
		  "s_initiative" : self.player.s_initiative,
		  "s_dexterity" : self.player.s_dexterity,
		  "start" : self.dialogue_engine.start,
		  "leave" : self.leave,
		  "continue_dialogue" : self.player.continue_dialogue
        }

        self.dialogue_engine.set_mapped_functions(funcs)
        self.dialogue_engine.start_new_dialogue("presentation_dialogue", self.player, Character("Maitre du jeu"))

        self.map.initialize_map()

    def begin_game(self):
        random_pos = [random.randint(0, self.map.dimension[0] - 1), random.randint(0, self.map.dimension[1] - 1)]
        self.map.set_treasure_tile(random_pos)
        self.map.set_tile_type(random_pos)
        self.map.player_on_tile(random_pos)
        self.player.set_pos(random_pos)

    def spawn_item(self):
        list_potions = self.dict_items["Potion"]
        max_luck = reduce(lambda x, y : x + y.drop, list_potions, 0.0)

        drop =  random.uniform(0.0, max_luck)

        for potion in list_potions[::-1]:
            max_luck -= potion.drop
            if drop > max_luck:
                return potion

    def generate_enemy_level(self, nb_enemy):
        max_num = self.player.level * 2
        max_lvl = self.player.level + 2
        mid_lvl = max_lvl - round(nb_enemy * max_lvl / max_num)
        return random.randint(max(1, mid_lvl - 2), mid_lvl + 2)

    def generate_enemy_name(self, lvl, index):
        if (lvl > 15):
            return colored_str("Géant " + str(index + 1), Color.RED)
        elif (lvl > 10):
            return colored_str("Ogre " + str(index + 1), Color.RED)
        elif (lvl >5):
            return colored_str("Gobelin " + str(index + 1), Color.RED)
        else:
            return colored_str("Slime " + str(index + 1), Color.RED)

    def generate_enemy(self, nb_enemy, index):
        result = self.generate_enemy_level(nb_enemy)
        result = [self.generate_enemy_name(result, index), result, random.randint(9, 19)]
        return result
    
    def spawn_enemy(self):
        nb_enemy = random.randint(1, self.player.level * 2)
        list_stat = [self.generate_enemy(nb_enemy, i) for i in range(nb_enemy)]
        enemies = [Enemy(stat[0], stat[1], True, stat[2]) for stat in list_stat]
        [enemy.add_attacks(self.dict_attacks["CHARACTER"] + self.dict_attacks["ENEMY"]) for enemy in enemies]

        # possible spawn de weapon
        
        return enemies

    def item_interaction(self, item):
        print("Tu as trouvé une " + str(item) + " !")
        result = bool(int(input("Veux tu la ramasser (0) ou non (1) : ")))

        if (result):
            return
        self.map.set_tile_type(self.player.pos)
        self.player.add_item(item)

    def initiative_sort(self, character_list):
        max_initiative = reduce(lambda x, y: x + y.initiative, character_list, 0)
        choosen_initiative = random.uniform(0.0, max_initiative)
        for character in character_list:
            max_initiative -= character.initiative
            if (choosen_initiative >= max_initiative):
                character_list.remove(character)
                return character

    def encounter(self, enemies):
        roll = random.randint(0, 2)
        choice = False

        if roll == 0:
            print("Dans ta chance, tu aperçois au loin un danger composé de " + str(enemies) + '.')
            choice = bool(int(input("Veux tu les affronter (0) ou non (1) : ")))
            if (choice):
                print("\nParfois la prudence est préférable. Tu contourne sans problème l'enemie.\n")
            else:
                print("\nTAYAUT!\n")
        elif roll == 1:
            print("Tu viens de tomber devant " + str(enemies) + '.')
            print("Heureusement pour toi, ils sont tout aussi surpris de te voir!")
            print("Tu peux donc essayer de fuir (réussite [1, 50], réussite + dégats subit [51, 65], échec [66, 100]).")
            choice = bool(int(input("Essaies tu de les affronter (0) ou non (1) : ")))
            if (choice):
                roll = random.randint(1, 100)
                print('\n' + self.player.name + " essaie de fuire : " + str(roll) + " / 100")
                if roll > 65:
                    print("\nEchec ! Le combat commence !\n")
                    choice = False
                elif roll > 50:
                    enemies[0].attack(enemies[0].choose_attack(self.dict_attacks["ENEMY"][1]), self.player)
                    if self.player.life > 0.0:
                        print("\nRéussite ! Malgré l'attaque sournoise tu arrive à t'enfuire.\n")
                else:
                    print("\nRéussite ! Tu t'en va le plus loin possible de ces vils monstre.\n")
            else:
                print("\nLe combat commence !\n")
        else:
            print("\nSans crier gare des enemis t'attaquent !")
            print("Le combat commence !\n")

        return choice
    
    def battle_round(self, characters, enemies):
        print("\n===================ROUND===================\n")
        self.player.update_potion_effect()
        print("\nOrdre de passage :")

        for character in characters:
            if (character.life > 0.0):
                print("\t- " + str(character))

        for character in characters:
            if character == self.player:
                target = character.choose_target(enemies)
                escape = character.attack(target, character.choose_attack())
                if escape:
                    return True
                if target.dead():
                    self.player.xp += 10 * target.level / self.player.level
                    self.player.level_up()
                    enemies.remove(target)
            elif character.life > 0.0:
                character.attack(self.player, character.choose_attack())
                if character.dead():
                    self.player.xp += 10 * character.level / self.player.level
                    self.player.level_up()
                    enemies.remove(character)

            if (not enemies):
                self.map.set_tile_type(self.player.pos)
                return True
            if (self.player.life <= 0.0):
                return True

        return False
        
    def enemy_interaction(self, enemies):
        l_character = [self.player] + enemies
        battle = self.encounter(enemies)
        end = False
        if (not battle):
            print("\n========================BATTLE========================\n")
            while not end:
                l_character = [self.initiative_sort(l_character) for i in range(len(l_character))]
                end = self.battle_round(l_character, enemies)
            if (self.player.life <= 0.0):
                return True
            self.player.draw_life()
            self.player.draw_xp()

    def check_tile(self):
        print("\n============================================================\n")
        player_pos = self.player.pos
        if self.map.map[player_pos[0]][player_pos[1]].tile_type == TileType.ITEM:
            item = self.spawn_item()
            self.item_interaction(item)
        elif self.map.map[player_pos[0]][player_pos[1]].tile_type == TileType.ENEMY:
            enemies = self.spawn_enemy()
            return self.enemy_interaction(enemies)
        elif self.map.map[player_pos[0]][player_pos[1]].tile_type == TileType.NONE:
            print("Il n'y a rien à cet endroit... Décevant!\n")
            sleep(0.3)
        else:
            print_colored("Bravo, tu as trouver le TVA (Trésor Virtuel Abyssal) !", Color.YELLOW)
            self.player.xp += 100
            self.map.set_tile_type(self.player.pos)
            self.map.set_treasure_tile(self.player.pos)
            return not bool(int(input("Tu as maintenant un choix crucial à faire, veux tu teminer ton aventure ici et rentrer chez toi en héro avec le trésor (0) ou bien préfères tu la posser toujours plus loin tes limites et chercher les autres trésors qui se cache dans cette contré (1) : ")))

    def game_round(self):
        refresh_map = True
        
        key = 0

        while(not self.end):
            if (refresh_map):
                self.map.player_on_tile(self.player.pos)
                self.map.draw(self.player.pos)
                self.map.player_on_tile(self.player.pos, False)
                print("(w = haut, a = gauche, s = bas, d = droite, q = quit)")
                refresh_map = False 

            key = kb.read_key(suppress=True)
            
            if key.lower() in {'a', 'd', 'w', 's'}:
                refresh_map = True
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

                self.end = self.check_tile()

            elif (key.lower() == 'q'):
                self.end = True
        
        if key == 0:
            return

        elif key.lower() == 'q':
            print("\nA la revoyure. En espérant que tu ais apprécié !")
            
        elif self.player.life > 0:
            print_colored("\nFélicitation ! Tu as trouvez le trésor perdu des limbes. Ainsi s'achève ton odyssée périlleuse. Au plaisir !", Color.GREEN)

        else:
            print_colored("\n... Qui aurait pu s'attendre à une telle mort... Il est encore temps de réessayer !", Color.RED)
            if bool(int(input("\nVeux tu réessayer (oui = 1): "))):
                print("\n\n")
                self.__init__()
                self.begin_game()
                self.game_round()


    # Simple function callback
    def leave(self, dialogue_engine, result):
        self.dialogue_engine.start_dialogue("stop_dialogue")
        self.end = True
