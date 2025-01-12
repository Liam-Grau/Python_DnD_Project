from enum import Enum
from src.Color import *


class StatType(Enum):
    LIFE = 0
    MAX_LIFE = 1
    CRT_MULTI = 2
    STRENGTH = 3
    RESISTANCE = 4
    INITIATIVE = 5
    DEXTERITY = 6


class Item:
    def __init__(self, name, stat: StatType = StatType.LIFE, efficiency=5, duration=3, drop=50):
        self.name = name
        self.stat = stat
        if type(self.stat) == int:
            self.stat = StatType(self.stat)
        
        self.efficiency = efficiency
        self.duration = duration
        self.drop = drop

    def __str__(self):
        return self.name + " Potion : [statistique affectée = " + self.stat.name + " , effet = +" + str(self.efficiency) + ", durée = " + str(self.duration) + ']'

    def __repr(self):
        return self.__str__()

    @property
    def __dict__(self):
        return {"name": self.name, "stat": self.stat.name, "efficiency": self.efficiency, "duration": self.duration, "drop": self.drop}


class PotionEffect:
    def __init__(self, stat=StatType.LIFE, duration=2.0, efficiency=1.0, name="HEAL"):
        self.stat = stat
        self.duration = duration
        self.efficiency = efficiency
        self.name = name

    @property
    def __dict__(self):
        return [self.stat.name, self.duration, self.efficiency, self.name]