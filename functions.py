import pygame
import button
import numpy as np

stat_modifier = {1:'-5', 2:'-4', 3:'-4', 4:'-3', 5:'-3', 6:'-2', 7:'-2', 8:'-1', 9:'-1', 10:'+0', 11:'+0', 12:'+1', 13:'+1', 14:'+2', 15:'+2', 16:'+3', 17:'+3', 18:'+4', 19:'+4', 20:'+5', 21:'+5', 22:'+6', 23:'+6', 24:'+7', 25:'+7'}

#Function to draw text on screen
def draw_text(text, font, color, x, y, screen):
    img = font.render(text, True, color)
    screen.blit(img, (x,y))

def draw_stats(STATS, stat_modifier, font, color, x, y, dy, screen):
    draw_text('Strength: ' + str(STATS[0]) + ' (' + stat_modifier[STATS[0]] + ')', font, color, x, y, screen)
    draw_text('Dexterity: ' + str(STATS[1]) + ' (' + stat_modifier[STATS[1]] + ')', font, color, x, y+dy, screen)
    draw_text('Constitution: ' + str(STATS[2]) + ' (' + stat_modifier[STATS[2]] + ')', font, color, x, y+(2*dy), screen)
    draw_text('Intelligence: ' + str(STATS[3]) + ' (' + stat_modifier[STATS[3]] + ')', font, color, x, y+(3*dy), screen)
    draw_text('Wisdom: ' + str(STATS[4]) + ' (' + stat_modifier[STATS[4]] + ')', font, color, x, y+(4*dy), screen)
    draw_text('Charisma: ' + str(STATS[5]) + ' (' + stat_modifier[STATS[5]] + ')', font, color, x, y+(5*dy), screen)


def text_wrap(text, font, color, surface, x, y, max_width):
    words = text.split(' ')
    lines = []
    line = ''
    for word in words:
        test_line = line + word + ' '
        if font.size(test_line)[0] < max_width:
            line = test_line
        else:
            lines.append(line)
            line = word + ' '
    lines.append(line)
    y_offset = 5
    for line in lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y + y_offset)
        surface.blit(text_surface, text_rect)
        y_offset += font.size(line)[1]



def dice_sound():
    i = np.random.randint(1,7)
    sound_name = 'Sounds/dice_roll_' + str(i) + '.wav'
    dice_roll_sound = pygame.mixer.Sound(sound_name)
    dice_roll_sound.set_volume(1.4)
    dice_roll_sound.play()


def d20(disadvantage=False, advantage=False):
    if (disadvantage and advantage) or (not disadvantage and not advantage):
        number = np.random.randint(1,21)
    elif disadvantage:
        number = min([np.random.randint(1,21), np.random.randint(1,21)])
    elif advantage:
        number = max([np.random.randint(1,21), np.random.randint(1,21)])
    return number



def combat(player, ENEMIES, screen, stat_font, text_col, font, clock):

    #Attack button
    attack_img = pygame.image.load('Pictures/attack.png').convert_alpha()
    attack_button = button.Button(300,600, attack_img, 0.4)

    #Initiative
    player_initiative = np.random.randint(1, 21) + int(stat_modifier[player.dex])

    enemy_initiatives = []
    for enemy in ENEMIES:
        enemy_initiative = np.random.randint(1, 21) + int(stat_modifier[enemy.dex])
        enemy_initiatives.append((enemy_initiative, enemy))

    all_initiatives = [(player_initiative, player)] + enemy_initiatives

    sorted_initiatives = sorted(all_initiatives, key=lambda x: x[0], reverse=True)

    WEAPONS = player.weapons()
    quitting = False

    
    while len(sorted_initiatives)>1 and player.alive==True and not quitting:

        for event in pygame.event.get():

            #Pause check
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = True
            #Quit check
            if event.type == pygame.QUIT:
                run = False
                quitting = True


        screen.fill((156, 115, 3))
        draw_text('Health: ' + str(player.hp), font, text_col, 50, 230, screen)
        
        dy = 30

        #Initiative order print
        i=0
        while i<len(sorted_initiatives):
            if i == 0:
                draw_text('Taking turn: ' + sorted_initiatives[i][1].name, font, text_col, 500, 80, screen)
                draw_text('Up next:', font, text_col, 500, 110, screen)
                
            else:
                draw_text(sorted_initiatives[i][1].name + ' ' + str(sorted_initiatives[i][1].hp) + 'hp', stat_font, text_col, 620, 115 + (i-1)*dy, screen)
                
            i+=1

        #Player turn
        
        if sorted_initiatives[0][1].name == player.name:
            


            if attack_button.draw(screen):
                #TODO: Add input for selecting one of multiple enemies with output index selected_enemy
                #TODO: Add option for selecting a weapon/spell from inventory to use in the attack
                selected_enemy = 1
                selected_weapon = 0

                #draw_text('Attack roll:     vs.' + str(sorted_initiatives[selected_enemy][1].ac) + 'AC', font, text_col, 100, 30, screen)
                

                dice_sound()
                attack_roll, crit = WEAPONS[selected_weapon].attack_roll(player)

                if attack_roll >= sorted_initiatives[selected_enemy][1].ac:

                    draw_text('Attack roll: ' + str(attack_roll) + ' vs. ' + str(sorted_initiatives[selected_enemy][1].ac) + 'AC', font, text_col, 100, 30, screen)
                    draw_text('Success!', font, text_col, 100, 60, screen)
                    pygame.display.update()
                    pygame.time.wait(2500)

                    damage = WEAPONS[selected_weapon].damage_roll(player, crit)
                    dice_sound()
                    draw_text(str(sorted_initiatives[selected_enemy][1].name) + ' takes ' + str(damage) + ' damage!', font, text_col, 100, 90, screen)
                    sorted_initiatives[selected_enemy][1].take_damage(damage)

                    if sorted_initiatives[selected_enemy][1].alive:
                        draw_text(str(sorted_initiatives[selected_enemy][1].name) + ' has ' + str(sorted_initiatives[selected_enemy][1].hp) + ' left', font, text_col, 100, 120, screen)
                        pygame.display.update()
                        pygame.time.wait(2500)
                        
                    else:
                        draw_text(str(sorted_initiatives[selected_enemy][1].name) + ' falls!', font, text_col, 100, 120, screen)
                        pygame.display.update()
                        pygame.time.wait(2500)
                        sorted_initiatives.pop(selected_enemy)

                else:
                    draw_text('Attack roll: ' + str(attack_roll) + ' vs. ' + str(sorted_initiatives[selected_enemy][1].ac) + 'AC', font, text_col, 100, 30, screen)
                    draw_text('You miss!',font, text_col, 100, 60, screen)
                    pygame.display.update()
                    pygame.time.wait(2500)
                
                sorted_initiatives.append(sorted_initiatives.pop(0))



        #Enemy turn
            
        else:

            
            enemy = sorted_initiatives[0][1]

            #draw_text('Attack roll:     vs.' + str(player.ac) + 'AC', font, text_col, 100, 30, screen)
            #pygame.time.wait(2500)

            dice_sound()
            attack_roll, crit = enemy.weapon.attack_roll(enemy)

            if attack_roll >= player.ac:

                draw_text('Attack roll: ' + str(attack_roll) + ' vs. ' + str(player.ac) + 'AC', font, text_col, 100, 30, screen)
                draw_text(enemy.name + ' hits you!', font, text_col, 100, 60, screen)
                pygame.display.update()
                pygame.time.wait(2500)

                damage = enemy.weapon.damage_roll(enemy, crit)
                dice_sound()
                draw_text(enemy.name + ' deals ' + str(damage) + ' damage!', font, text_col, 100, 90, screen)
                player.take_damage(damage)

                if player.alive:
                    draw_text('You withstand the attack!', font, text_col, 100, 120, screen)
                    pygame.display.update()
                    pygame.time.wait(2500)
                    
                else:
                    draw_text('YOU DIED!', font, text_col, 100, 120, screen)
                    pygame.display.update()
                    pygame.time.wait(2500)

            else:
                draw_text('Attack roll: ' + str(attack_roll) +     ' vs.' + str(player.ac) + 'AC', font, text_col, 100, 30, screen)
                draw_text(enemy.name + ' missed you!',font, text_col, 100, 60, screen)
                pygame.display.update()
                pygame.time.wait(2500)

            sorted_initiatives.append(sorted_initiatives.pop(0))

        pygame.display.update()
        clock.tick(60)

            
# ------------------------------------------------------------------------------------------------------------------------------------------------
# SPECIAL ENCOUNTERS
# ------------------------------------------------------------------------------------------------------------------------------------------------

