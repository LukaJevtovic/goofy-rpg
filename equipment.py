import numpy as np
import pygame
import functions
import button

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
    
    def get_button(self, creature, x, y, scale):

        font1 = pygame.font.SysFont(None, 35)
        font2 = pygame.font.SysFont(None, 25)

        text1 = self.name

        atk_bonus = int(stat_modifier[getattr(creature, self.stat, None)]) + creature.proficiency_bonus()
        if creature.name == 'Player':
            if creature.race == 'orc' and self.melee:
                atk_bonus+=1
            if creature.race == 'elf' and not self.melee:
                atk_bonus+=1

        if atk_bonus>=0:
            text2 = 'ATK: ' + '+' + str(atk_bonus)
        else:
            text2 = 'ATK: ' + str(atk_bonus)


        dmg_bonus = int(stat_modifier[getattr(creature, self.stat, None)])
        if creature.name == 'Player':
            if creature.race == 'orc' and self.melee:
                dmg_bonus+=1
            if creature.race == 'elf' and not self.melee:
                dmg_bonus+=1

        if dmg_bonus>=0:
            text3 = ' DMG: ' + self.damage_die + '+' + str(dmg_bonus)
        else:
            text3 = ' DMG:' + self.damage_die + str(dmg_bonus)

        # Render each piece of text onto separate surfaces
        text_surface1 = font1.render(text1, True, (0,0,0))
        text_surface2 = font2.render(text2, True, (0,0,0))
        text_surface3 = font2.render(text3, True, (0,0,0))

        # Get the dimensions of the text surfaces
        text_width1, text_height1 = text_surface1.get_size()
        text_width2, text_height2 = text_surface2.get_size()
        text_width3, text_height3 = text_surface3.get_size()

        #Get the dimensions of the total surface
        total_width = max(text_width1, text_width2 + text_width3)
        total_height = text_height1 + text_height2

        combined_surface = pygame.Surface((total_width, total_height))
        combined_surface.fill((255,255,255))

        #Blit weapon info onto surface
        combined_surface.blit(text_surface1, (0,0))
        combined_surface.blit(text_surface2, (0,text_height1))
        combined_surface.blit(text_surface3, (text_width2, text_height1))

        total_button = button.ButtonSlow(x,y,combined_surface, scale)

        return total_button

    def get_ButtonOnce(self, creature, x, y, scale):
        font1 = pygame.font.SysFont(None, 35)
        font2 = pygame.font.SysFont(None, 25)

        text1 = self.name

        atk_bonus = int(stat_modifier[getattr(creature, self.stat, None)]) + creature.proficiency_bonus()
        if creature.name == 'Player':
            if creature.race == 'orc' and self.melee:
                atk_bonus+=1
            if creature.race == 'elf' and not self.melee:
                atk_bonus+=1

        if atk_bonus>=0:
            text2 = 'ATK: ' + '+' + str(atk_bonus)
        else:
            text2 = 'ATK: ' + str(atk_bonus)


        dmg_bonus = int(stat_modifier[getattr(creature, self.stat, None)])
        if creature.name == 'Player':
            if creature.race == 'orc' and self.melee:
                dmg_bonus+=1
            if creature.race == 'elf' and not self.melee:
                dmg_bonus+=1

        if dmg_bonus>=0:
            text3 = ' DMG: ' + self.damage_die + '+' + str(dmg_bonus)
        else:
            text3 = ' DMG:' + self.damage_die + str(dmg_bonus)

        # Render each piece of text onto separate surfaces
        text_surface1 = font1.render(text1, True, (0,0,0))
        text_surface2 = font2.render(text2, True, (0,0,0))
        text_surface3 = font2.render(text3, True, (0,0,0))

        # Get the dimensions of the text surfaces
        text_width1, text_height1 = text_surface1.get_size()
        text_width2, text_height2 = text_surface2.get_size()
        text_width3, text_height3 = text_surface3.get_size()

        #Get the dimensions of the total surface
        total_width = max(text_width1, text_width2 + text_width3)
        total_height = text_height1 + text_height2

        combined_surface = pygame.Surface((total_width, total_height))
        combined_surface.fill((255,255,255))

        #Blit weapon info onto surface
        combined_surface.blit(text_surface1, (0,0))
        combined_surface.blit(text_surface2, (0,text_height1))
        combined_surface.blit(text_surface3, (text_width2, text_height1))

        selected_surface = pygame.Surface((total_width, total_height))
        selected_surface.fill((138, 138, 138))

        #Blit weapon info onto surface
        selected_surface.blit(text_surface1, (0,0))
        selected_surface.blit(text_surface2, (0,text_height1))
        selected_surface.blit(text_surface3, (text_width2, text_height1))

        total_button = button.ButtonOnce(x,y,combined_surface, selected_surface, scale)

        return total_button

            
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
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def get_ButtonOnce(self, creature, x, y, scale):
        font = pygame.font.SysFont(None, 35)
        text = str(self.value) + self.name

        text_surface = font.render(text, True, (0,0,0))
        combined_surface = pygame.Surface(text_surface.get_size())
        combined_surface.fill((255,255,255))
        combined_surface.blit(text_surface, (0,0))

        selected_surface = pygame.Surface(text_surface.get_size())
        selected_surface.fill((138, 138, 138))
        selected_surface.blit(text_surface, (0,0))


        total_button = button.ButtonOnce(x,y,combined_surface, selected_surface, scale)

        return total_button





class Spell():
    def __init__(self, mana_cost, spell_level, offensive):
        self.mana_cost = mana_cost
        self.level = spell_level
        self.offensive = offensive




shortsword = Weapon('Shortsword', 'dex', 0, 'd6', True)
longsword = Weapon('Longsword', 'str', 0, 'd8', True)
longbow = Weapon('Longbow', 'dex', 0, 'd8', False)
firebolt = Weapon('Firebolt', 'int', 0, 'd10', False)

goblin_cleaver = Weapon('Goblin Scimitar', 'dex', 1, 'd10', True)

robes = Armor('Clothes', 'Light', 10, True)
breastplate = Armor('Breastplate', 'Medium', 14, True)
full_plate = Armor('Full Plate', 'Heavy', 18, False)

shield = Shield('Shield')

gold_pouch = Item('50 gold', 50)


LOOT1 = [Item('gold', 50), Item('gold', 20), Item('gold', 10), shortsword, longbow, longsword]

LOOT4 = [Item('gold', 200), Item('gold', 100), longsword, goblin_cleaver]
