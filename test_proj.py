from src.Game import *

def test_DragonAndDungeon_test():
    p = Player("Liam", 10)
    m = Map()
    e = Enemy("Antoine", 2)
    i = Item("La popo")
    
    assert type(p) == Player
    assert type(m) == Map
    assert type(e) == Enemy
    assert type(i) == Item
