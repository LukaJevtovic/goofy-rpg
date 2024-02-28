import pygame
import button
import numpy as np

stat_modifier = {1:'-5', 2:'-4', 3:'-4', 4:'-3', 5:'-3', 6:'-2', 7:'-2', 8:'-1', 9:'-1', 10:'+0', 11:'+0', 12:'+1', 13:'+1', 14:'+2', 15:'+2', 16:'+3', 17:'+3', 18:'+4', 19:'+4', 20:'+5', 21:'+5', 22:'+6', 23:'+6', 24:'+7', 25:'+7'}

#Function to draw text on screen
def draw_text(text, font, color, x, y, screen):
    img = font.render(text, True, color)
    width = img.get_width()
    screen.blit(img, (x,y))
    return width





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


        screen.fill((229,203,186))
        #draw_text('Health: ' + str(player.hp), font, text_col, 50, 230, screen)
        
        health_bar(player, 20, 20, 0, (255,255,255), screen)
        xp_bar(player, 20, 20, (255,255,255), screen)
        dy = 30

        #Initiative order print
        i=0
        while i<len(sorted_initiatives):
            if i == 0:
                width = draw_text('Taking turn: ' + sorted_initiatives[i][1].name, font, text_col, 500, 80, screen)
                if not sorted_initiatives[i][1].name == 'Player':
                    health_bar(sorted_initiatives[i][1], 500 + width, 77, 1, (255,255,255), screen)
                draw_text('Up next:', font, text_col, 500, 110, screen)
                
            else:
                width = draw_text(sorted_initiatives[i][1].name, stat_font, text_col, 620, 115 + (i-1)*dy, screen)

                if not sorted_initiatives[i][1].name == 'Player':
                    health_bar(sorted_initiatives[i][1], 625 + width, 112 + (i-1)*dy, 1, (255,255,255), screen)
                
            i+=1

        #Player turn
        selected_enemy = -1

        
        if sorted_initiatives[0][1].name == player.name:

            while selected_enemy == -1 and not quitting:

                for event in pygame.event.get():

                    #Pause check
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            selected_enemy = 1
                        elif event.key == pygame.K_2:
                            if len(sorted_initiatives)>2:
                                selected_enemy = 2
                        elif event.key == pygame.K_3:
                            if len(sorted_initiatives)>3:
                                selected_enemy = 3
                    #Quit check
                    if event.type == pygame.QUIT:
                        run = False
                        quitting = True

                screen.fill((229,203,186))
                #draw_text('Health: ' + str(player.hp), font, text_col, 50, 230, screen)
                
                health_bar(player, 20, 20, 0, (255,255,255), screen)
                xp_bar(player, 20, 20, (255,255,255), screen)
                dy = 30

                #Initiative order print
                i=0
                while i<len(sorted_initiatives):
                    if i == 0:
                        width = draw_text('Taking turn: ' + sorted_initiatives[i][1].name, font, text_col, 500, 80, screen)
                        if not sorted_initiatives[i][1].name == 'Player':
                            health_bar(sorted_initiatives[i][1], 500 + width, 77, 1, (255,255,255), screen)
                        draw_text('Up next:', font, text_col, 500, 110, screen)
                        
                    else:
                        width = draw_text(sorted_initiatives[i][1].name, stat_font, text_col, 620, 115 + (i-1)*dy, screen)

                        if not sorted_initiatives[i][1].name == 'Player':
                            health_bar(sorted_initiatives[i][1], 625 + width, 112 + (i-1)*dy, 1, (255,255,255), screen)
                        
                    i+=1

                draw_text('Select enemy to attack! [Buttons 1-' + str(len(sorted_initiatives)-1) + ']', font, text_col, 200, 500, screen)

                pygame.display.update()
                clock.tick(60)
                        
            

            if selected_enemy != -1:
                #TODO: Add option for selecting a weapon/spell from inventory to use in the attack
                selected_weapon = 0

                #draw_text('Attack roll:     vs.' + str(sorted_initiatives[selected_enemy][1].ac) + 'AC', font, text_col, 100, 30, screen)
                

                dice_sound()
                attack_roll, crit = WEAPONS[selected_weapon].attack_roll(player)

                if attack_roll >= sorted_initiatives[selected_enemy][1].ac:

                    draw_text('Attack roll: ' + str(attack_roll) + ' vs. ' + str(sorted_initiatives[selected_enemy][1].ac) + 'AC', font, text_col, 300, 300, screen)
                    draw_text('Success!', font, text_col, 300, 330, screen)
                    pygame.display.update()
                    pygame.time.wait(2500)

                    damage = WEAPONS[selected_weapon].damage_roll(player, crit)
                    dice_sound()
                    draw_text(str(sorted_initiatives[selected_enemy][1].name) + ' takes ' + str(damage) + ' damage!', font, text_col, 300, 360, screen)
                    sorted_initiatives[selected_enemy][1].take_damage(damage)

                    if sorted_initiatives[selected_enemy][1].alive:
                        draw_text(str(sorted_initiatives[selected_enemy][1].name) + ' has ' + str(sorted_initiatives[selected_enemy][1].hp) + ' left', font, text_col, 300, 390, screen)
                        pygame.display.update()
                        pygame.time.wait(2500)
                        
                    else:
                        draw_text(str(sorted_initiatives[selected_enemy][1].name) + ' falls!', font, text_col, 300, 390, screen)
                        
                        if player.race == 'human':
                            draw_text('You gain ' + str(int(1.1*sorted_initiatives[selected_enemy][1].xp)) + ' xp!', font, text_col, 300, 420, screen)
                            player.xp += int(1.1*sorted_initiatives[selected_enemy][1].xp)
                        else:
                            draw_text('You gain ' + str(int(sorted_initiatives[selected_enemy][1].xp)) + ' xp!', font, text_col, 300, 420, screen)
                            player.xp += int(sorted_initiatives[selected_enemy][1].xp)
                        pygame.display.update()
                        pygame.time.wait(2500)
                        sorted_initiatives.pop(selected_enemy)

                else:
                    draw_text('Attack roll: ' + str(attack_roll) + ' vs. ' + str(sorted_initiatives[selected_enemy][1].ac) + 'AC', font, text_col, 300, 300, screen)
                    draw_text('You miss!',font, text_col, 300, 330, screen)
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

                draw_text('Attack roll: ' + str(attack_roll) + ' vs. ' + str(player.ac) + 'AC', font, text_col, 300, 300, screen)
                draw_text(enemy.name + ' hits you!', font, text_col, 300, 330, screen)
                pygame.display.update()
                pygame.time.wait(2500)

                damage = enemy.weapon.damage_roll(enemy, crit)
                dice_sound()
                draw_text(enemy.name + ' deals ' + str(damage) + ' damage!', font, text_col, 300, 360, screen)
                player.take_damage(damage)

                if player.alive:
                    draw_text('You withstand the attack!', font, text_col, 300, 390, screen)
                    pygame.display.update()
                    pygame.time.wait(2500)
                    
                else:
                    draw_text('YOU DIED!', font, text_col, 300, 390, screen)
                    pygame.display.update()
                    pygame.time.wait(2500)

            else:
                draw_text('Attack roll: ' + str(attack_roll) +     ' vs.' + str(player.ac) + 'AC', font, text_col, 300, 300, screen)
                draw_text(enemy.name + ' missed you!',font, text_col, 300, 330, screen)
                pygame.display.update()
                pygame.time.wait(2500)

            sorted_initiatives.append(sorted_initiatives.pop(0))

        pygame.display.update()
        clock.tick(60)


def leveling_menu(player, font, color, screen, clock):
    leveling = True
    animation = False
    quitting = False

    continue_img = pygame.image.load('Pictures/continue.png').convert_alpha()
    continue_button = button.ButtonSlow(600, 600, continue_img, 0.3)

    while leveling and not quitting:

        for event in pygame.event.get():

            #Pause check
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = True
            #Quit check
            if event.type == pygame.QUIT:
                run = False
                quitting = True



        screen.fill((229,203,186))
        
        health_bar(player, 20, 20, 0, (255,255,255), screen)
        xp_bar(player, 20, 20, (255,255,255), screen)

        draw_text('Level up!', font, color, 400, 20, screen)


        if not animation:

            pygame.mixer.Sound('Sounds/levelup.mp3').play()

            draw_text('HP: ' + str(player.max_hp), font, color, 100, 200, screen)
            pygame.display.update()
            clock.tick(60)
            pygame.time.wait(1000)

            draw_text('HP: ' + str(player.max_hp) + ' ->', font, color, 100, 200, screen)
            pygame.display.update()
            clock.tick(60)
            pygame.time.wait(1000)
            
            old_hp = player.max_hp
            animation = True

            if player.dnd_class == 'fighter':
                draw_text('HP: ' + str(player.max_hp) + ' ->' + ' ' + str(player.max_hp + 6), font, color, 100, 200, screen)
                player.max_hp+=6
                player.hp+=6
                player.lvl = 2
                pygame.display.update()
                clock.tick(60)
                pygame.time.wait(1000)
            elif player.dnd_class == 'wizard':
                draw_text('HP: ' + str(player.max_hp) + ' ->' + ' ' + str(player.max_hp + 4), font, color, 100, 200, screen)
                player.max_hp+=4
                player.hp+=4
                player.lvl = 2
                pygame.display.update()
                clock.tick(60)
                pygame.time.wait(1000)

        draw_text('HP: ' + str(old_hp) + ' ->' + ' ' + str(player.max_hp), font, color, 100, 200, screen)

        if continue_button.draw(screen):
            quitting = True


        pygame.display.update()
        clock.tick(60)


#type = 0-player, 1-in-combat
def health_bar(creature, x, y, type, stat_col, screen):
    if type==0:
        hp_font = pygame.font.SysFont(None, 30)
        background_width = 45 + creature.max_hp*2
        active_width = background_width*(creature.hp/creature.max_hp)

        pygame.draw.rect(screen, (0,0,0), (20, 45, background_width, 25))
        pygame.draw.rect(screen, (255,0,0),(21,46,active_width, 23))
        draw_text(str(creature.hp) + '/' + str(creature.max_hp), hp_font, stat_col, 22, 48, screen)

    elif type==1:
        hp_font = pygame.font.SysFont(None, 25)
        background_width = 25 + creature.max_hp
        active_width = background_width*(creature.hp/creature.max_hp)

        pygame.draw.rect(screen, (0,0,0), (x,y, background_width, 25))
        pygame.draw.rect(screen, (255,0,0),(x,y+1,active_width, 23))
        draw_text(str(creature.hp) + '/' + str(creature.max_hp), hp_font, stat_col, x+2, y+3, screen)

def xp_bar(player, x, y, col, screen):

    xp_font = pygame.font.SysFont(None, 30)
    background_width = 200

    if player.xp >= player.xp_to_lvlup():
        active_width = background_width
    else:
        active_width = background_width*(player.xp/player.xp_to_lvlup())

    pygame.draw.rect(screen, (0,0,0), (x, y, background_width, 25))
    pygame.draw.rect(screen, (179,161,48),(x+1, y+1, active_width, 23))
    draw_text(str(player.xp) + '/' + str(player.xp_to_lvlup()), xp_font, col, x+2, y+3, screen)



# ------------------------------------------------------------------------------------------------------------------------------------------------
# SPECIAL ENCOUNTERS
# ------------------------------------------------------------------------------------------------------------------------------------------------


