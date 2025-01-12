from src.Color import *

class Weapon:
    def __init__(self, name, damage = 5, drop = 0.5):
        self.name = name
        self.damage = damage
        self.drop = drop

    def __str__(self):
        return self.name + " : [Damage = " + str(self.damage) + ", Drop chance = " + str(self.drop) + ']'

    def __repr__(self):
        return self.__str__

    @property
    def __dict__(self):
        return {"name": self.name, "damage": self.damage, "drop": self.drop}
