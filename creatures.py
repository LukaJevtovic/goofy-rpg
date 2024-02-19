import numpy as np
import equipment

class Player():
    def __init__(self, hp, AC, str, dex, con, int, wis, cha):
        self.total_health = hp
        self.ac = AC
        self.str = str
        self.dex = dex
        self.con = con
        self.int = int
        self.wis = wis
        self.cha = cha
        self.hp = self.total_health

    def take_damage(self, amount):
        dead = False
        self.hp -= amount
        if self.hp<=0:
            self.hp = 0
            dead = True
        
        return dead
    
class basic_enemy():
    def __init__(self, hp, AC, str, dex, con, int, wis, cha, weapon, atk_bonus, dmg_bonus):
        self.total_health = hp
        self.ac = AC
        self.str = str
        self.dex = dex
        self.con = con
        self.int = int
        self.wis = wis
        self.cha = cha
        self.hp = self.total_health
        self.weapon = weapon
        self.atk_bonus = atk_bonus
        self.dmg_bonus = dmg_bonus
    
    def take_damage(self, amount):
        dead = False
        self.hp -= amount
        if self.hp<=0:
            self.hp = 0
            dead = True
        
        return dead
    

goblin = basic_enemy(7, 15, 8, 14, 10, 10, 8, 8, equipment.longsword, 4, 2)

            