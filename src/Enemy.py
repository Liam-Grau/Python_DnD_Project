from src.Character import *

class Enemy(Character):
    def __init__(self, name, level=1, r=True, nb_point=19):
        super(Enemy, self).__init__(name, level, r, nb_point)
        
    def __str__(self):
        return super(Enemy, self).__str__()

    def __repr__(self):
        return "Enemy: " + self.__str__()

    def choose_attack(self, prohibited_attacks=[]):
        attack_pool = [attack for attack in self.attacks if attack not in prohibited_attacks]
        return attack_pool[random.randint(0, len(attack_pool) - 1)]

    def dead(self):
        if (self.life > 0.0):
            return False

        print('\n' + self.name + " est mort!")
        return True
