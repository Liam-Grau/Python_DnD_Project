from msilib.schema import _Validation_records
import random
from abc import ABC, abstractmethod
from turtle import st
from src.Attack import *
from src.Color import *
from src.Weapon import *


class Character:
    def __init__(self, name = "?????", level=1, r=True, nb_point=19):
        self.name = name
        self.level = level
        self.nb_point = nb_point
        self.nb_point += level

        self.max_life = 1
        self.life = 1
        self.crt_multi = 1

        self.strength = 0
        self.resistance = 0
        self.initiative = 0
        self.dexterity = 0

        if r:
            self.randomize_attributes()

        self.weapon = None
        self.attacks = []
        self.calculate_stats()

    def randomize_attributes(self):
         max_nb_point = self.nb_point

         self.strength = random.randint(0, min(max_nb_point // 2,  self.nb_point))
         self.nb_point -= self.strength
         self.resistance = random.randint(0, min(max_nb_point // 2,  self.nb_point))
         self.nb_point -= self.resistance
         self.initiative = random.randint(0, min(max_nb_point // 2,  self.nb_point))
         self.nb_point -= self.initiative
         self.dexterity = random.randint(0, min(max_nb_point // 2,  self.nb_point))
         self.nb_point -= self.dexterity

    def calculate_stats(self):
        self.max_life = self.level * (self.resistance + self.initiative) * 0.5 + 1
        self.life = self.max_life
        self.crt_multi = 1 + (self.dexterity + self.strength) * 0.1

    def s_name(self, name):
        self.name = colored_str(name, Color.GREEN)
        return True

    def s_strength(self, strength):

        try:
            value = int(strength)
        except ValueError:
            return False

        if self.nb_point >= 0 and value <= self.nb_point:
            self.strength += value
            self.nb_point -= value
            return True

        return False

    def s_resistance(self, resistance):

        try:
            value = int(resistance)
        except ValueError:
            return False

        if self.nb_point >= 0 and value <= self.nb_point:
            self.resistance += value
            self.nb_point -= value
            return True

        return False

    def s_initiative(self, initiative):

        try:
            value = int(initiative)
        except ValueError:
            return False

        if self.nb_point >= 0 and value <= self.nb_point:
            self.initiative += value
            self.nb_point -= value
            return True

        return False

    def s_dexterity(self, dexterity):

        try:
            value = int(dexterity)
        except ValueError:
            return False

        if self.nb_point >= 0 and value <= self.nb_point:
            self.dexterity += value
            self.nb_point -= value
            return True

        return False

    def __str__(self):
        return "[Name : " + self.name + ", Level : " + str(self.level) + ", Strength : " + str(self.strength) + ", Resistance : " + str(self.resistance) + ", Initiative : " + str(self.initiative) + ", Dexterity : " + str(self.dexterity) + ", Life : " + str(self.life) + " / " + str(self.max_life) + ", Critical Multiplicator : " + str(self.crt_multi) + ']'

    def __repr__(self):
        return "Character: " + self.__str__()

    def attribute_statistics(self, nb_point):
            print("C'est le moment de repartir tes points de maitrise, tu en as " +
                  str(nb_point) + " de disponible.")
            test = True
            max_nb_point = nb_point

            while (test):
                print("Tu as encore " + str(nb_point) + " points a depenser.")
                strength = abs(int(input("Nombre de point dans strength (augmente ton attaque et tes dégâts critiques) : ")))
                self.strength += strength
                nb_point -= strength
                
                print("Tu as encore " + str(nb_point - self.strength) + " points a depenser.")
                resistance = abs(int(input("Nombre de point dans resistance (diminue tes dégâts subits et augmente ta vie) : ")))
                self.resistance += resistance
                nb_point -= resistance
                
                print("Tu as encore " + str(nb_point) + " points a depenser.")
                initiative = abs(int(input("Nombre de point dans initiative (augmente tes chances de commencer un combat et ta vie) : ")))
                self.initiative += initiative
                nb_point -= initiative
                
                print("Tu as encore " + str(nb_point) + " points a depenser.")
                dexterity = abs(int(input("Nombre de point dans dexterity (augmente tes chances d'esquive et tes dégâts critiques) : ")))
                self.dexterity += dexterity
                nb_point -= dexterity

                if (nb_point < 0):
                    print("Tricheur!")
                    print("On recommence")
                    nb_point = max_nb_point

                elif nb_point > 0:
                    test = not bool(int(input("Il te reste des points, veux tu malgré tout finaliser la création de ton personnage (oui = 1, non = 0) : ")))
                    max_nb_point = nb_point

                else:
                    print("Personnage cree!")
                    test = False
                    

            self.max_life = self.level * (self.resistance + self.initiative) * 0.5 + 1.0
            self.life = self.max_life
            self.crt_multi = 1 + (self.dexterity + self.strength) * 0.1

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
            weapon_damage = self.weapon.damage

        if roll > attack.failure:
            print_colored("Echec critique !", Color.RED)
            damage = max((attack.damage + self.strength + weapon_damage) * self.crt_multi - self.resistance, 0)
            print('\n' + self.name + " s'inflige " + str(damage) + " points de dégat !\n")
            self.life -= damage
        elif roll > attack.success:
            print_colored("Echec.", Color.ORANGE)
            return
        elif roll > attack.crt:
            print_colored("Réussite.", Color.GREEN)
            if (other_character.dodge(self)):
                return
            damage = max(attack.damage + self.strength + weapon_damage - other_character.resistance, 0)
            print('\n' + self.name + " inflige " + str(damage) + " points de dégat à " + other_character.name + " !\n")
            other_character.life -= damage
        else:
            print_colored("Réussite Critique !", Color.YELLOW)
            if (other_character.dodge(self, True)):
                return
            damage = max((attack.damage + self.strength + weapon_damage) * self.crt_multi - other_character.resistance, 0)
            print('\n' + self.name + " inflige " + str(damage) + " points de dégat à " + other_character.name + " !\n")
            other_character.life -= damage
