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

        self.potion_effect += [[potion.stat, potion.duration, potion.efficiency, potion.name]]

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
            effect[1] -= 1
            
            if effect[0] == StatType.LIFE and effect[1] > 0:
                self.life = min(self.max_life, self.life + effect[2])
                print("Tu as été soigné de " + str(effect[2]) + " pv.")

            if (effect[1] == 0):
                expire_effect += [effect]
                if (effect[0] == StatType.LIFE):
                    print("L'effet de ta " + effect[3] + " Potion vient d'expirer. Tu ne seras plus soigné.")
                if (effect[0] == StatType.CRT_MULTI):
                    self.crt_multi -= effect[2]
                    print("L'effet de ta " + effect[3] + " Potion vient d'expirer. Ta statistique revient à sa valeur initial (multiplicateur critique = " + self.crt_multi + ").")
                elif (effect[0] == StatType.STRENGTH):
                    self.strength -= effect[2]
                    print("L'effet de ta " + effect[3] + " Potion vient d'expirer. Ta statistique revient à sa valeur initial (force = " + self.strength + ").")
                elif (effect[0] == StatType.RESISTANCE):
                    self.resistance -= effect[2]
                    print("L'effet de ta " + effect[3] + " Potion vient d'expirer. Ta statistique revient à sa valeur initial (résistance = " + self.resistance + ").")
                elif (effect[0] == StatType.INITIATIVE):
                    self.initiative -= effect[2]
                    print("L'effet de ta " + effect[3] + " Potion vient d'expirer. Ta statistique revient à sa valeur initial (initiative = " + self.initiative + ").")
                elif (effect[0] == StatType.DEXTERITY):
                    self.dexterity -= effect[2]
                    print("L'effet de ta " + effect[3] + " Potion vient d'expirer. Ta statistique revient à sa valeur initial (dextérité = " + self.dexterity + ").")

        self.potion_effect = [effect for effect in self.potion_effect if effect not in expire_effect]
        
