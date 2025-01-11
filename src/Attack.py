class Attack:
    def __init__(self, name, damage, crt = 5, success = 50, failure = 96):
        self.name = name
        self.damage = damage
        self.crt = crt
        self.success = success
        self.failure = failure

    def __str__(self):
        return "[Name : " + self.name + ", Damage : " + str(self.damage) + ", Critic Success : 0-" + str(self.crt) + ", Success : " + str(self.crt + 1) + '-' + str(self.success) + ", Failure : " + str(self.success + 1) + '-' + str(self.failure) + ", Critic Failure : " + str(self.failure + 1) + "-100]"

    def __repr__(self):
        return "Attack: " + self.__str__()
        
