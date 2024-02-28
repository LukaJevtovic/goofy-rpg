import numpy as np
import functions

stat_modifier = {1:'-5', 2:'-4', 3:'-4', 4:'-3', 5:'-3', 6:'-2', 7:'-2', 8:'-1', 9:'-1', 10:'+0', 11:'+0', 12:'+1', 13:'+1', 14:'+2', 15:'+2', 16:'+3', 17:'+3', 18:'+4', 19:'+4', 20:'+5', 21:'+5', 22:'+6', 23:'+6', 24:'+7', 25:'+7'}

def dice(die_type):

    if die_type == 'd4':
        return 1, 5
    elif die_type == 'd6':
        return 1, 7
    elif die_type == 'd8':
        return 1,9
    elif die_type == 'd10':
        return 1,11
    elif die_type == 'd12':
        return 1, 13
    elif die_type == 'd20':
        return 1, 21

class Weapon():
    def __init__(self, name, stat, enchanted, damage_die, melee):
        self.name = name
        self.stat = stat
        self.enchanted = enchanted
        self.damage_die = damage_die
        self. melee = melee
        if self.enchanted != 0:
            self.enchantment = self.enchanted
        else:
            self.enchantment = 0

    def attack_roll(self, creature, advantage=False, disadvantage=False):

        atk_bonus = int(stat_modifier[getattr(creature, self.stat, None)]) + creature.proficiency_bonus()
        
        if creature.name == 'Player':
            if creature.race == 'orc' and self.melee:
                atk_bonus+=1
            if creature.race == 'elf' and not self.melee:
                atk_bonus+=1
        
        atk_dice = functions.d20(advantage, disadvantage)
        print(atk_dice)

        if atk_dice == 20:
            crit = True
        else:
            crit = False
        return atk_dice + self.enchantment + atk_bonus, crit
            

    def damage_roll(self, creature, crit):
        dmg_bonus = int(stat_modifier[getattr(creature, self.stat, None)])

        minimum, maximum = dice(self.damage_die)
        if crit:
            damage = 2*np.random.randint(minimum, maximum) + dmg_bonus + self.enchantment
        else:
            damage = np.random.randint(minimum, maximum) + dmg_bonus + self.enchantment

        if creature.name == 'Player':
            if creature.race == 'orc' and self.melee:
                damage+=1
            if creature.race == 'elf' and not self.melee:
                damage+=1
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

class Item():
    def __init__(self, name):
        self.name = name
    
shortsword = Weapon('Shortsword', 'dex', 0, 'd6', True)
longsword = Weapon('Longsword', 'str', 0, 'd8', True)
longbow = Weapon('Longbow', 'dex', 0, 'd8', False)
firebolt = Weapon('Firebolt', 'int', 0, 'd10', False)

robes = Armor('Clothes', 'Light', 10, True)
breastplate = Armor('Breastplate', 'Medium', 14, True)
full_plate = Armor('Full Plate', 'Heavy', 18, False)

shield = Shield('Shield')

gold_pouch = Item('50 gold')
