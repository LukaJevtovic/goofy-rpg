import pygame
import numpy as np
import creatures
import button
import equipment
import functions
from functools import partial

stat_modifier = {1:'-5', 2:'-4', 3:'-4', 4:'-3', 5:'-3', 6:'-2', 7:'-2', 8:'-1', 9:'-1', 10:'+0', 11:'+0', 12:'+1', 13:'+1', 14:'+2', 15:'+2', 16:'+3', 17:'+3', 18:'+4', 19:'+4', 20:'+5', 21:'+5', 22:'+6', 23:'+6', 24:'+7', 25:'+7'}


class Spell():
    def __init__(self, name, spell_function, mana_cost, description):
        self.name = name
        self.mana_cost = mana_cost
        self.description = description

        self.spell_function = spell_function
    
    def get_button(self, x, y, scale, max_width, desc_x, desc_y, desc_scale, just_dimensions=False):
        font1 = pygame.font.SysFont(None, 35)
        font2 = pygame.font.SysFont(None, 20)

        text1 = self.name
        text2 = self.description

        text_surface1 = font1.render(text1, True, (0,0,0))

        text_width1, text_height1 = text_surface1.get_size()

        combined_surface = pygame.Surface((text_width1, text_height1))
        combined_surface.fill((69,136,245))

        combined_surface.blit(text_surface1, (0,0))

        if just_dimensions:
            return combined_surface.get_size()

        selected_surface = pygame.Surface((text_width1, text_height1))
        selected_surface.fill((69,136,245)) #TODO: Add darker shade of blue (17,60,130) when you figure out .clicked handling in combat

        selected_surface.blit(text_surface1, (0,0))

        desc_surface = functions.text_wrap_surface(text2, font2, (0,0,0), max_width)

        total_button = button.SpellButton(x,y,combined_surface, selected_surface, desc_surface, desc_x, desc_y, desc_scale, scale)

        return total_button


def firebolt_function(player, sorted_initiatives, selected_enemy, font, text_col, log_x, log_y, screen):

    d20_roll = functions.d20()

    if d20_roll == 20:
        crit = True
    else:
        crit = False

    attack_roll = functions.d20() + int(stat_modifier[player.int]) + player.proficiency_bonus()
    functions.dice_sound()

    if attack_roll >= sorted_initiatives[selected_enemy][1].ac:

            functions.draw_text('Attack roll: ' + str(attack_roll) + ' vs. ' + str(sorted_initiatives[selected_enemy][1].ac) + 'AC', font, text_col, log_x, log_y, screen)
            functions.draw_text('Success!', font, text_col, log_x, log_y + 30, screen)
            pygame.display.update()
            pygame.time.wait(2500)

            if crit:
                damage = 2*np.random.randint(1,13) + int(stat_modifier[player.int])
            else:
                damage = np.random.randint(1,13) + int(stat_modifier[player.int])
            functions.dice_sound()
            functions.draw_text(str(sorted_initiatives[selected_enemy][1].name) + ' takes ' + str(damage) + ' damage!', font, text_col, log_x, log_y + 60, screen)
            sorted_initiatives[selected_enemy][1].take_damage(damage)

            if sorted_initiatives[selected_enemy][1].alive:
                functions.draw_text(str(sorted_initiatives[selected_enemy][1].name) + ' has ' + str(sorted_initiatives[selected_enemy][1].hp) + ' left', font, text_col, log_x, log_y + 90, screen)
                pygame.display.update()
                pygame.time.wait(2500)
                    
            else:
                functions.draw_text(str(sorted_initiatives[selected_enemy][1].name) + ' falls!', font, text_col, log_x, log_y + 90, screen)
                        
                if player.race == 'human':
                    functions.draw_text('You gain ' + str(int(1.1*sorted_initiatives[selected_enemy][1].xp)) + ' xp!', font, text_col, log_x, log_y + 120, screen)
                    player.xp += int(1.1*sorted_initiatives[selected_enemy][1].xp)
                else:
                    functions.draw_text('You gain ' + str(int(sorted_initiatives[selected_enemy][1].xp)) + ' xp!', font, text_col, log_x, log_y + 120, screen)
                    player.xp += int(sorted_initiatives[selected_enemy][1].xp)
                pygame.display.update()
                pygame.time.wait(2500)
                sorted_initiatives.pop(selected_enemy)

    else:
        functions.draw_text('Attack roll: ' + str(attack_roll) + ' vs. ' + str(sorted_initiatives[selected_enemy][1].ac) + 'AC', font, text_col, log_x, log_y, screen)
        functions.draw_text('You miss!',font, text_col, log_x, log_y + 30, screen)
        pygame.display.update()
        pygame.time.wait(2500)

    player.mp-=2
    sorted_initiatives.append(sorted_initiatives.pop(0))

def fire_breath_function(player, sorted_initiatives, selected_enemy, font, text_col, log_x, log_y, screen):

    save_dc = 8 + player.proficiency_bonus() + int(stat_modifier[player.int])

    damage = np.random.randint(1,7) + np.random.randint(1,7) + np.random.randint(1,7) + int(stat_modifier[player.int])
    functions.dice_sound()

    functions.draw_text('Full damage: ' + str(damage), font, text_col, log_x, log_y, screen)
    functions.draw_text('Enemies try to dodge!', font, text_col, log_x, log_y + 30, screen)
    pygame.display.update()
    pygame.time.wait(2500)

    j=2
    i=0
    while i < len(sorted_initiatives):
        
        if sorted_initiatives[i][1].name != 'Player':
            local_roll = functions.d20()
            print(local_roll)
            save_roll = local_roll + int(stat_modifier[sorted_initiatives[i][1].dex])
            functions.dice_sound()

            functions.draw_text(sorted_initiatives[i][1].name + ' rolls ' + str(save_roll) + ' vs. ' + str(save_dc), font, text_col, log_x, log_y + j*30, screen)
            j+=1
            pygame.display.update()
            pygame.time.wait(2500)

            if save_roll>=save_dc:
                local_dmg = int(damage/2)
            else:
                local_dmg = damage
            
            functions.draw_text(sorted_initiatives[i][1].name + ' takes ' + str(local_dmg) + ' damage!', font, text_col, log_x, log_y + j*30, screen)
            j+=1
            pygame.display.update()
            pygame.time.wait(2500)

            if sorted_initiatives[i][1].take_damage(local_dmg):
                
                functions.draw_text(sorted_initiatives[i][1].name + ' falls! You gain ' + str(sorted_initiatives[i][1].xp) + ' xp!', font, text_col, log_x, log_y + j*30, screen)
                j+=1
                player.xp += sorted_initiatives[i][1].xp
                sorted_initiatives.pop(i)
                i-=1
                pygame.display.update()
                pygame.time.wait(2500)
            
            else:
                functions.draw_text(sorted_initiatives[i][1].name + ' is still standing!', font, text_col, log_x, log_y + j*30, screen)
                j+=1
                pygame.display.update()
                pygame.time.wait(2500)

        i+=1
    
    player.mp-=6
    sorted_initiatives.append(sorted_initiatives.pop(0))

            

            


            









fire_breath = Spell('Fire breath', fire_breath_function, 6, 'Engulf all your foes in flame. INT based spell that costs 6 to cast. Targets all enemies (select any one of them and the spell will hit them all). All enemies make a DEX save to try and halve 3d6 + INT damage.')

firebolt = Spell('Firebolt', firebolt_function, 2, 'Shoot a fiery projectile at a single target. Cheap cost of 2 mana makes it easy to cast often. INT-based spell that deals 1d12 + INT damage on a hit.')