import numpy as np

def dice(die_type):

    if die_type == 'd4':
        return 1, 5
    elif die_type == 'd6':
        return 1, 7
    elif die_type == 'd8':
        return 1,9
    elif die_type == 'd12':
        return 1, 13
    elif die_type == 'd20':
        return 1, 21

class Weapon():
    def __init__(self, name, melee, enchanted, damage_die):
        self.name = name
        self.melee = melee
        self.enchanted = enchanted
        self.damage_die = damage_die
        if self.enchanted != 0:
            self.enchantment = self.enchanted
        else:
            self.enchantment = 0

    def attack_roll(self, atk_bonus, threatened):

        if self.melee:
            if threatened:
                atk_dice = np.random.randint(1,21)
                if atk_dice == 20:
                    crit = True
                else:
                    crit = False
                return atk_dice + self.enchantment + atk_bonus, crit
            else:
                return 0
        if not self.melee:
            if threatened:
                atk_dice = min(np.random.randint(1,21), np.random.randint(1,21))
                if atk_dice == 20:
                    crit = True
                else:
                    crit = False
                return atk_dice + self.enchantment + atk_bonus, crit
            else:
                atk_dice = np.random.randint(1,21)
                if atk_dice == 20:
                    crit = True
                else:
                    crit = False
                return atk_dice + self.enchantment + atk_bonus, crit
            
    def damage_roll(self, dmg_bonus, crit):
        minimum, maximum = dice(self.damage_die)
        if crit:
            damage = 2*np.random.randint(minimum, maximum) + dmg_bonus + self.enchantment
        else:
            damage = np.random.randint(minimum, maximum) + dmg_bonus + self.enchantment
        return damage
            
class Armor():
    def __init__(self, name, type, base_ac, stealthy):
        self.name = name
        self.type = type
        self.ac = base_ac
        self.stealthy = stealthy

    def is_stealthy(self):
        return self.stealthy
    
    def find_ac(self, dex_bonus):
        if self.type == 'Light':
            return self.ac + dex_bonus
        elif self.type == 'Medium':
            if dex_bonus <= 2:
                return self.ac+dex_bonus
            else:
                return self.ac + 2
        elif self.type == 'Heavy':
            return self.ac
        
class Shield():
    def __init__(self, name):
        self.name = name
    

longsword = Weapon('Longsword',True, 0, 'd8')
longbow = Weapon('Longbow', False, 0, 'd8')
firebolt = Weapon('Firebolt', False, 0, 'd10')

robes = Armor('Clothes', 'Light', 10, True)
breastplate = Armor('Breastplate', 'Medium', 14, True)
full_plate = Armor('Full Plate', 'Heavy', 18, False)

shield = Shield('Shield')