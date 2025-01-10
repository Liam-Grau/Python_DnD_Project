from src.Character import *


class Player(Character):

    def __init__(self, name, level=1, random=True, min_point=1, max_point=10):
        super(Player, self).__init__(name, level, random, min_point, max_point)
        self.xp = 0
        self.max_xp = 100
        self.pos = [0, 0]

    def set_pos(self, new_pos):
        self.pos = new_pos
