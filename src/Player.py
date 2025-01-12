from src.Character import *
from src.Item import *
from src.DialogueEngine import *

class Player(Character):

    def __init__(self, name="?????", level=1, random=False, nb_point=19):
        super(Player, self).__init__(name, level, random, nb_point)
        self.xp = 0
        self.max_xp = 100
        self.pos = [0, 0]
        self.inventory = []
        self.quantity = []
        self.potion_effect = []

    def save(self):
        saved_player = vars(self)

        inventory = list(map(lambda item: item.__dict__, saved_player["inventory"]))
        saved_player["inventory"] = inventory

        if self.weapon != None:
            saved_player["weapon"] = self.weapon.__dict__

        potion_effect = list(map(lambda effect: effect.__dict__, saved_player["potion_effect"]))
        saved_player["potion_effect"] = potion_effect

        attacks = list(map(lambda attack: attack.__dict__, saved_player["attacks"]))
        saved_player["attacks"] = attacks

        with open("data/saved_player.json", "w") as file:
            json.dump(saved_player, file, indent = 4)

    def get_saved_player(self):
        try:
            with open("data/saved_player.json", "r") as file:
                saved_player = json.load(file)
            self.xp = saved_player.get("xp", 0)
            self.max_xp = saved_player.get("max_xp", 100)
            self.pos = saved_player.get("pos", [0, 0])
            self.quantity = saved_player.get("quantity", [])
            self.life = saved_player.get("life", 1)
            self.max_life = saved_player.get("max_life", 1)
            self.crt_multi = saved_player.get("crt_multi", 1)
            self.strength = saved_player.get("strenght", 0)
            self.resistance = saved_player.get("resistance", 0)
            self.initiative = saved_player.get("initiative", 0)
            self.dexterity = saved_player.get("dexterity", 0)

            for i in range(len(saved_player["inventory"])): 
                item = saved_player["inventory"][i]
                self.inventory.append(Item(item["name"], StatType[item["stat"]], item["efficiency"], item["duration"], item["drop"]))

            for i in range(len(saved_player["potion_effect"])):
                effect = saved_player["potion_effect"][i]
                self.potion_effect.append(PotionEffect(StatType[effect[0]] , effect[1], effect[2], effect[3]))

            for i in range(len(saved_player["attacks"])):
                attack = saved_player["attacks"][i]
                self.attacks.append(Attack(attack["name"], attack["damage"], attack["crt"], attack["success"], attack["failure"]))

            if saved_player["weapon"] != None:
                self.weapon = Weapon(saved_player["weapon"]["name"], saved_player["weapon"]["damages"], saved_player["weapon"]["drop"])
       
            self.name = saved_player.get("name")
            self.level = saved_player.get("level", 1)
            self.nb_point = saved_player.get("nb_point", 19)
            print("Joueur chargé avec succès !")
        except FileNotFoundError:
            print("Aucune sauvegarde trouvée.")

    def delete_save(self):
        os.remove("data/saved_player.json")

    def choose_target(self, opponents):
        print("\nQuel monstre veux tu attaquer :")

        for i in range(len(opponents)):
            print("\t- " + str(i + 1) + " : " + str(opponents[i]))

        choice = int(input('\n')) - 1

        return opponents[choice]
    
    def choose_stats(self, dialogue_engine, value):
        dialogue_engine.start_dialogue("point_repartition_dialogue")

    def random_stats(self, dialogue_engine, value):
        dialogue_engine.start_dialogue("final_dialogue")
        self.randomize_attributes()
        self.calculate_stats()

    def continue_dialogue(self, dialogue_engine, value):
        dialogue_engine.start_dialogue("final_dialogue")
        self.calculate_stats()

    def choose_attack(self, prohibited_attacks=[]):
        attack_pool = [attack for attack in self.attacks if attack not in prohibited_attacks]
        self.draw_life()
        self.draw_xp()
    
        choice = bool(int(input("\nVeux tu prendre une potion (cela ne passera pas ton tour) (oui = 1, non = 0) : ")))

        if choice:
            potion_time = True
            while (potion_time):
                print("\nQuelle objet veux tu utiliser :")
                for i in range(len(self.inventory)):
                    if self.quantity[i]:
                        print("\t- " + str(i + 1) + " : " + str(self.inventory[i]) + " (x" + str(self.quantity[i]) + ')')
                choice = int(input('\n Si tu entre un index autre, tu sors de ton inventaire : ')) - 1
                potion_time = self.apply_potion_effect(choice)
        
        print("\nQuelle attaque veux tu utiliser :")

        for i in range(len(attack_pool)):
            print("\t- " + str(i + 1) + " : " + str(self.attacks[i]))

        choice = int(input('\n')) - 1

        return attack_pool[choice]

    def attack(self, other_character, attack):
        if (attack.name == "Escape"):
            roll = random.randint(1, 100)
            print('\n' + self.name + " essaie de s'enfuir du combat (réussite 50 %) : " + str(roll) + " / 100")
            if (roll < 51):
                print_colored("Réussite.", Color.GREEN)
                return True
            else:
                print_colored("Echec.", Color.RED)
            
        else:
            super(Player, self).attack(other_character, attack)

        return False

    def set_pos(self, new_pos):
        self.pos = new_pos

    def add_item(self, item):
        if item in self.inventory:
            self.quantity[self.inventory.index(item)] += 1

        else:
            self.inventory += [item]
            self.quantity += [1]

    def draw_life(self):
        print("\nVie : " + str(self.life) + " / " + str(self.max_life))

    def draw_xp(self):
        print("\nExpérience : " + str(self.xp) + " / " + str(self.max_xp) + '\n')
    
    def level_up(self):
        if (self.xp > self.max_xp):
            nb_point = 2 * self.xp // self.max_xp
            self.level += nb_point // 2
            self.xp %= self.max_xp
            self.life = self.max_life
            self.draw_life()
            self.draw_xp()

            self.attribute_statistics(nb_point)
            

    def apply_potion_effect(self, index_potion):
        if (index_potion < 0 or index_potion > len(self.inventory) - 1):
            return False

        potion = self.inventory[index_potion]
        self.quantity[index_potion] -= 1
        if  (self.quantity[index_potion] == 0):
            del self.quantity[index_potion]
            del self.inventory[index_potion]
            
        print(potion.name + " Potion utilisée.")

        self.potion_effect += [PotionEffect(potion.stat, potion.duration, potion.efficiency, potion.name)]

        if (potion.stat == StatType.LIFE):
            self.life = min(self.max_life, self.life + potion.efficiency)
            print("Tu as été soigné de " + str(potion.efficiency) + " pv.")
        elif (potion.stat == StatType.CRT_MULTI):
            self.crt_multi += potion.efficiency
            print("Ton multiplicateur critique a été augmenter de " + str(potion.efficiency) + ". Ta stat est maintenant égale à " + str(self.crt_multi) + '.')
        elif (potion.stat == StatType.STRENGTH):
            self.strength += potion.efficiency
            print("Ta force a été augmenter de " + str(potion.efficiency) + ". Ta stat est maintenant égale à " + str(self.strength) + '.')
        elif (potion.stat == StatType.RESISTANCE):
            self.resistance += potion.efficiency
            print("Ta résistance a été augmenter de " + str(potion.efficiency) + ". Ta stat est maintenant égale à " + str(self.resistance) + '.')
        elif (potion.stat == StatType.INITIATIVE):
            self.initiative += potion.efficiency
            print("Ton initiative a été augmenter de " + str(potion.efficiency) + ". Ta stat est maintenant égale à " + str(self.initiative) + '.')
        elif (potion.stat == StatType.DEXTERITY):
            self.dexterity += potion.efficiency
            print("Ta dextérité a été augmenter de " + str(potion.efficiency) + ". Ta stat est maintenant égale à " + str(self.dexterity) + '.')

        return True
            

    def update_potion_effect(self):
        expire_effect = []
        
        for effect in self.potion_effect:
            effect.duration -= 1
            
            if effect.stat == StatType.LIFE and effect.duration > 0:
                self.life = min(self.max_life, self.life + effect.efficiency)
                print("Tu as été soigné de " + str(effect.efficiency) + " pv.")

            if (effect.duration == 0):
                expire_effect += [effect]
                if (effect.stat == StatType.LIFE):
                    print("L'effet de ta " + effect.name+ " Potion vient d'expirer. Tu ne seras plus soigné.")
                if (effect.stat == StatType.CRT_MULTI):
                    self.crt_multi -= effect.efficiency
                    print("L'effet de ta " + effect.name + " Potion vient d'expirer. Ta statistique revient à sa valeur initial (multiplicateur critique = " + str(self.crt_multi) + ").")
                elif (effect.stat == StatType.STRENGTH):
                    self.strength -= effect.efficiency
                    print("L'effet de ta " + effect.name + " Potion vient d'expirer. Ta statistique revient à sa valeur initial (force = " + str(self.strength) + ").")
                elif (effect.stat == StatType.RESISTANCE):
                    self.resistance -= effect.efficiency
                    print("L'effet de ta " + effect.name + " Potion vient d'expirer. Ta statistique revient à sa valeur initial (résistance = " + str(self.resistance) + ").")
                elif (effect.stat == StatType.INITIATIVE):
                    self.initiative -= effect.efficiency
                    print("L'effet de ta " + effect.name + " Potion vient d'expirer. Ta statistique revient à sa valeur initial (initiative = " + str(self.initiative) + ").")
                elif (effect.stat == StatType.DEXTERITY):
                    self.dexterity -= effect.efficiency
                    print("L'effet de ta " + effect.name + " Potion vient d'expirer. Ta statistique revient à sa valeur initial (dextérité = " + str(self.dexterity) + ").")

        self.potion_effect = [effect for effect in self.potion_effect if effect not in expire_effect]
        
