import random
from abc import ABC, abstractmethod
from src.Attack import *
from src.Color import *


class Character:
    def __init__(self, name, level=1, r=True, nb_point=19):
        self.name = name
        self.level = level
        nb_point += level
        max_nb_point = nb_point  

        if r:
            self.strength = random.randint(0, min(max_nb_point // 2,  nb_point))
            nb_point -= self.strength
            self.resistance = random.randint(0, min(max_nb_point // 2,  nb_point))
            nb_point -= self.resistance
            self.initiative = random.randint(0, min(max_nb_point // 2,  nb_point))
            nb_point -= self.initiative
            self.dexterity = random.randint(0, min(max_nb_point // 2,  nb_point))

        else:
            nb_point = 2 * max_point
            print("C'est le moment de repartir tes points de maitrise, tu en as " +
                  str(nb_point) + " de disponible.")
            test = True

            while (test):
                print("Tu as encore " + str(nb_point) + " points a depenser.")
                self.strength = abs(int(input("Nombre de point dans strength : ")))
                print("Tu as encore " + str(nb_point - self.strength) + " points a depenser.")
                self.resistance = abs(int(input("Nombre de point dans resistance : ")))
                print("Tu as encore " + str(nb_point - self.strength -
                      self.resistance) + " points a depenser.")
                self.initiative = abs(int(input("Nombre de point dans initiative : ")))
                print("Tu as encore " + str(nb_point - self.strength -
                      self.resistance - self.initiative) + " points a depenser.")
                self.dexterity = abs(int(input("Nombre de point dans dexterity : ")))

                if (self.strength + self.resistance + self.initiative + self.dexterity <= nb_point):
                    print("Personnage cree!")
                    test = False

                else:
                    print("Tricheur!")

        self.max_life = self.level * (self.resistance + self.initiative) * 0.5
        self.life = self.max_life
        self.crt_multi = 1 + (self.dexterity + self.strength) * 0.1

        self.weapon = None
        self.attacks = []

    def __str__(self):
        return "[Name : " + self.name + ", Level : " + str(self.level) + ", Strength : " + str(self.strength) + ", Resistance : " + str(self.resistance) + ", Initiative : " + str(self.initiative) + ", Dexterity : " + str(self.dexterity) + ", Life : " + str(self.life) + " / " + str(self.max_life) + ", Critical Multiplicator : " + str(self.crt_multi) + ']'

    def __repr__(self):
        return "Character: " + self.__str__()

    def set_weapon(self, weapon):
        self.weapon = weapon

    def add_attacks(self, attacks):
        self.attacks += attacks

    def remove_attacks(self, attacks):
        self.attacks = [attack for attack in self.attacks if not attack in attacks]

    @abstractmethod
    def choose_attack(self, prohibited_attacks=[]):
       pass

    def dodge(self, other_character, penality = False):
        roll  = random.randint(1, 100)

        if (penality):
            print('\n' + self.name + " essaie d'esquiver mais ça ne sera pas aisé (5 % réussite) : " + str(roll) + " / 100")
            if (roll > 5):
                print_colored("Echec.", Color.RED)
            else:
                print_colored("Réussite critique !", Color.YELLOW)
                print('\n' + self.name + " s'en sort in extremis !")
                return True

        else:
            success = min(max(round(self.dexterity * 100 /(max(self.dexterity + other_character.dexterity, 1))), 5), 95)
            print('\n' + self.name + " essaie d'esquiver (" + str(success) + " % réussite)  : " + str(roll) + " / 100")
            if (roll > success):
                print_colored("Echec.", Color.RED)
            else:
                print_colored("Réussite.", Color.GREEN)
                print('\n' + self.name + " esquive l'attaque")
                return True
    
    def attack(self, other_character, attack):
        roll = random.randint(1, 100)
        weapon_damage = 0
        damage = 0

        print('\n' + self.name + " utilise " + attack.name + " sur " + other_character.name + " : " + str(roll) + " / 100")

        if (self.weapon):
            weapon_damage = weapon.damage

        if roll > attack.failure:
            print_colored("Echec critique !", Color.RED)
            damage = (attack.damage + self.strength + weapon_damage) * self.crt_multi - self.resistance
            print('\n' + self.name + " s'inflige " + str(damage) + " points de dégat !\n")
            self.life -= damage
        elif roll > attack.success:
            print_colored("Echec.", Color.ORANGE)
            return
        elif roll > attack.crt:
            print_colored("Réussite.", Color.GREEN)
            if (other_character.dodge(self)):
                return
            damage = attack.damage + self.strength + weapon_damage - other_character.resistance
            print('\n' + self.name + " inflige " + str(damage) + " points de dégat à " + other_character.name + " !\n")
            other_character.life -= damage
        else:
            print_colored("Réussite Critique !", Color.YELLOW)
            if (other_character.dodge(self, True)):
                return
            damage = (attack.damage + self.strength + weapon_damage) * self.crt_multi - other_character.resistance
            print('\n' + self.name + " inflige " + str(damage) + " points de dégat à " + other_character.name + " !\n")
            other_character.life -= damage
