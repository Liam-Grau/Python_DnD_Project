import random
from src.Attack import *


class Character:
    def __init__(self, name, level=1, r=True, min_point=1, max_point=10):
        self.name = name
        self.level = level

        if r:
            self.strength = random.randint(min_point, max_point)
            self.resistance = random.randint(min_point, max_point)
            self.initiative = random.randint(min_point, max_point)
            self.dexterity = random.randint(min_point, max_point)

        else:
            nb_point = 2 * max_point
            print("C'est le moment de repartir tes points de maitrise, tu en as " +
                  str(nb_point) + " de disponible.")
            test = True

            while (test):
                print("Tu as encore " + str(nb_point) + "points a depenser.")
                self.strength = abs(int(input("Nombre de point dans strength : ")))
                print("Tu as encore " + str(nb_point - self.strength) + "points a depenser.")
                self.resistance = abs(int(input("Nombre de point dans resistance : ")))
                print("Tu as encore " + str(nb_point - self.strength -
                      self.resistance) + "points a depenser.")
                self.initiative = abs(int(input("Nombre de point dans initiative : ")))
                print("Tu as encore " + str(nb_point - self.strength -
                      self.resistance - self.initiative) + "points a depenser.")
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

    def add_attacks(self, attacks):
        self.attacks += attacks

    def attack(self, index, other_character):
        attack = self.attacks[index]
        roll = random.randint(1, 100)
        weapon_damage = 0

        if (self.weapon):
            weapon_damage = weapon.damage

        if roll > attack.failure:
            self.life -= (attack.damage + strength + weapon_damage) * self.crt_multi
        elif roll > attack.success:
            return
        elif roll > attack.crt:
            other_character -= attack.damage + strength + weapon_damage
        else:
            other_character -= (attack.damage + strength + weapon_damage) * self.crt_multi
