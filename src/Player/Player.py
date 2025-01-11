from src.Character import *


class Player(Character):

    def __init__(self, name, level=1, random=True, nb_point=19):
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
    
    def choose_attack(self, prohibited_attacks=[]):
        attack_pool = [attack for attack in self.attacks if attack not in prohibited_attacks]
        self.draw_life()
    
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
        self.draw_xp()

        if (self.xp > self.max_xp):
            self.level += self.xp // self.max_xp
            self.xp %= self.max_xp

    def apply_potion_effect(self, index_potion):
        if (index_potion < 0 or index_potion > len(self.inventory) - 1):
            return False

        potion = self.inventory[index_potion]
        print(potion.name + " Potion utilisée.")

        self.potion_effect += [[potion.stat, potion.duration, potion.efficiency, potion.name]]

        if (potion.stat == 0):
            self.life = min(self.max_life, self.life + potion.efficiency)
        elif (potion.stat == 2):
            self.crt_multi += potion.efficiency
        elif (potion.stat == 3):
            self.strength += potion.efficiency
        elif (potion.stat == 4):
            self.resistance += potion.efficiency
        elif (potion.stat == 5):
            self.initiative += potion.efficiency
        elif (potion.stat == 6):
            self.dexterity += potion.efficiency

        return True
            

    def update_potion_effect(self):
        expire_effect = []
        
        for effect in self.potion_effect:
            if effect[0] == 0:
                self.life = min(self.max_life, self.life + potion.efficiency)

            effect[1] -= 1
            if (effect[1] == 0):
                expire_effect += [effect]
        # to do
