import numpy as np
import equipment

#proficiency_bonus = {1:2, 2:2, 3:2, 4:2, 5:3, 6:3, 7:3, 8:3, 9:4, 10:4, 11:4, 12:4, 13:5, 14:5, 15:5, 16:5, 17:6, 18:6, 19:6, 20:6}
lvlup_xp = {1:300, 2:900, 3:2700, 4:6500}

class Player():
    def __init__(self, lvl, xp, hp, AC, str, dex, con, int, wis, cha, P_EQUIPMENT):
        self.name = 'Player'
        self.lvl = lvl
        self.max_hp = hp
        self.xp = xp
        self.dnd_class = ''
        self.race = ''

        self.ac = AC
        self.str = str
        self.dex = dex
        self.con = con
        self.int = int
        self.wis = wis
        self.cha = cha

        self.hp = self.max_hp
        self.equipment = P_EQUIPMENT
        self.alive = True

    def xp_to_lvlup(self):
        return lvlup_xp[self.lvl]


    def proficiency_bonus(self):
        if self.lvl < 5:
            return 2
        elif self.lvl < 9:
            return 3
        elif self.lvl < 13:
            return 4
        elif self.lvl < 17:
            return 5
        else:
            return 6
        
    def weapons(self):
        WEAPONS = [item for item in self.equipment if isinstance(item, equipment.Weapon)]
        return WEAPONS


    #def attack_roll(self, selected_weapon):
    #    self.weapons[selected_weapon].attack_roll(self)

    #def damage_roll(self, selected_weapon):
    #    self.weapons[selected_weapon].damage_roll()


    def take_damage(self, amount):
        dead = False
        self.hp -= amount
        if self.hp<=0:
            self.hp = 0
            dead = True
            self.alive = False
        
        return dead
    
class basic_enemy():
    def __init__(self, name, xp, hp, AC, str, dex, con, int, wis, cha, weapon, proficiency):
        self.name = name
        self.xp = xp
        self.max_hp = hp
        self.ac = AC
        self.str = str
        self.dex = dex
        self.con = con
        self.int = int
        self.wis = wis
        self.cha = cha
        self.hp = self.max_hp
        self.proficiency = proficiency
        self.weapon = weapon
        self.alive = True

    def proficiency_bonus(self):
        return self.proficiency
    
    def take_damage(self, amount):
        dead = False
        self.hp -= amount
        if self.hp<=0:
            self.hp = 0
            dead = True
            self.alive = False
        
        return dead
    
goblin_stats = ['Goblin', 50, 7, 15, 8, 14, 10, 10, 8, 8, equipment.shortsword, 2]
goblin_brute_stats = ['Goblin brute', 100, 18, 9, 16, 8, 16, 8, 8, 8, equipment.firebolt, 4]
goblin_brute = basic_enemy('Goblin brute', 100, 18, 9, 16, 8, 16, 8, 8, 8, equipment.firebolt, 4)
#goblin = basic_enemy('goblin', 7, 15, 8, 14, 10, 10, 8, 8, equipment.shortsword, 4, 2)


#p = Player(1, 10, 10, 10, 25, 10, 10, 10, 10, [equipment.shortsword])
