import pygame
import button
import equipment
import spellbook
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

def text_wrap_surface(text, font, color, max_width):
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
    total_height = sum(font.size(line)[1] for line in lines)
    surface = pygame.Surface((max_width, total_height), pygame.SRCALPHA)
    y_offset = 0
    for line in lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (0, y_offset)
        surface.blit(text_surface, text_rect)
        y_offset += font.size(line)[1]
    return surface


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

def combat(player, ENEMIES, screen, stat_font, text_col, font, clock, run):

    #Attack button
    attack_img = pygame.image.load('Pictures/attack.png').convert_alpha()
    attack_button = button.Button(350,500, attack_img, 0.4)

    #Initiative
    player_initiative = np.random.randint(1, 21) + int(stat_modifier[player.dex])

    enemy_initiatives = []
    for enemy in ENEMIES:
        enemy_initiative = np.random.randint(1, 21) + int(stat_modifier[enemy.dex])
        enemy_initiatives.append((enemy_initiative, enemy))

    all_initiatives = [(player_initiative, player)] + enemy_initiatives

    sorted_initiatives = sorted(all_initiatives, key=lambda x: x[0], reverse=True)

    
    #Position of log lines
    log_x = 20
    log_y = 110
    #Position of initiative lines
    init_x = 600
    init_y = 50

    WPN_BUTTONS = []
    SPELL_BUTTONS = []
    x = 20
    y = 600
    i=0
    
    if isinstance(player.right_hand, equipment.Weapon):
        WPN_BUTTONS.append(player.right_hand.get_button(player, x+i*200, y, 1))
        i+=1
    if isinstance(player.left_hand, equipment.Weapon):
        WPN_BUTTONS.append(player.left_hand.get_button(player, x+i*200, y, 1))
        i+=1

    for spell in player.spells:
        if x+i*200 <= 800:
            SPELL_BUTTONS.append(spell.get_button(x+i*200, y, 1.5, 500, log_x, log_y, 1))
            i+=1
        else:
            y+=100
            i=0
            SPELL_BUTTONS.append(spell.get_button(x+i*200, y, 1.5, 500, log_x, log_y, 1))
            i+=1

        
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
        
        health_bar(player, 20, 20, 0, (255,255,255), screen)
        xp_bar(player, 20, 20, (255,255,255), screen)
        mana_bar(player, 20, 70, (255,255,255), screen)
        dy = 30

        #Initiative order print
        i=0
        while i<len(sorted_initiatives):
            if i == 0:
                width = draw_text('Taking turn: ' + sorted_initiatives[i][1].name, font, text_col, init_x, init_y, screen)
                if not sorted_initiatives[i][1].name == 'Player':
                    health_bar(sorted_initiatives[i][1], init_x + width, init_y - 3, 1, (255,255,255), screen)
                draw_text('Up next:', font, text_col, init_x, init_y + 30, screen)
                
            else:
                width = draw_text(sorted_initiatives[i][1].name, stat_font, text_col, init_x + 120, init_y + 35 + (i-1)*dy, screen)

                if not sorted_initiatives[i][1].name == 'Player':
                    health_bar(sorted_initiatives[i][1], init_x + 125 + width, init_y + 32 + (i-1)*dy, 1, (255,255,255), screen)
                
            i+=1

        #Player turn
        selected_enemy = -1
        selected_weapon = -1
        selected_spell = False

        locked_in = False

        
        if sorted_initiatives[0][1].name == player.name:

            while not locked_in and not quitting:

                for event in pygame.event.get():
                    #Quit check
                    if event.type == pygame.QUIT:
                        run = False
                        quitting = True

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
                    

                screen.fill((229,203,186))
                
                health_bar(player, 20, 20, 0, (255,255,255), screen)
                xp_bar(player, 20, 20, (255,255,255), screen)
                mana_bar(player, 20, 70, (255,255,255), screen)
                dy = 30

                #Initiative order print
                i=0
                while i<len(sorted_initiatives):
                    if i == 0:
                        width = draw_text('Taking turn: ' + sorted_initiatives[i][1].name, font, text_col, init_x, init_y, screen)
                        if not sorted_initiatives[i][1].name == 'Player':
                            health_bar(sorted_initiatives[i][1], init_x + width, init_y - 3, 1, (255,255,255), screen)
                        draw_text('Up next:', font, text_col, init_x, init_y + 30, screen)
                        
                    else:
                        width = draw_text(sorted_initiatives[i][1].name, stat_font, text_col, init_x + 120, init_y + 35 + (i-1)*dy, screen)

                        if not sorted_initiatives[i][1].name == 'Player':
                            health_bar(sorted_initiatives[i][1], init_x + 125 + width, init_y + 32 + (i-1)*dy, 1, (255,255,255), screen)
                        
                    i+=1

                if selected_enemy == -1:
                    draw_text('Select enemy to attack! [Buttons 1-' + str(len(sorted_initiatives)-1) + ']', font, text_col, log_x, log_y + 300, screen)
                else:
                    draw_text('Selected enemy: ' + str(selected_enemy),font, text_col, log_x, log_y + 300, screen)

                if selected_weapon == -1 and selected_spell == False:
                    draw_text('Choose an attack!', font, text_col, log_x, log_y + 330, screen)
                elif selected_weapon == 0:
                    draw_text('Chosen attack: ' + player.right_hand.name, font, text_col, log_x, log_y + 330, screen)
                elif selected_weapon == 1:
                    draw_text('Chosen attack: ' + player.left_hand.name, font, text_col, log_x, log_y + 330, screen)
                elif selected_spell:
                    draw_text('Chosen attack: ' + spell.name, font, text_col, log_x, log_y + 330, screen)

                for wpn_button in WPN_BUTTONS:
                    if wpn_button.draw(screen):
                        selected_weapon = WPN_BUTTONS.index(wpn_button)

                i=0
                while i < len(SPELL_BUTTONS):
                    if SPELL_BUTTONS[i].draw(screen):
                        if player.mp >= player.spells[i].mana_cost:
                            selected_spell = True
                            spell = player.spells[i]
                        else:
                            draw_text('You don\'t have enough mana!', font, text_col, log_x, log_y + 270, screen)
                            pygame.display.update()
                            pygame.time.wait(1000)
                    i+=1

                if selected_weapon != -1 and selected_enemy != -1:
                    if attack_button.draw(screen):
                        locked_in = True

                if selected_spell and selected_enemy != -1:
                    if attack_button.draw(screen):
                        locked_in = True 
                pygame.display.update()
                clock.tick(60)

            
            if selected_weapon == 0 or selected_weapon == 1:
                dice_sound()
                if selected_weapon == 0:
                    attack_roll, crit = player.right_hand.attack_roll(player)
                elif selected_weapon == 1:
                    attack_roll, crit = player.left_hand.attack_roll(player)


                if attack_roll >= sorted_initiatives[selected_enemy][1].ac:

                    draw_text('Attack roll: ' + str(attack_roll) + ' vs. ' + str(sorted_initiatives[selected_enemy][1].ac) + 'AC', font, text_col, log_x, log_y, screen)
                    draw_text('Success!', font, text_col, log_x, log_y + 30, screen)
                    pygame.display.update()
                    pygame.time.wait(2500)

                    damage = player.right_hand.damage_roll(player, crit)
                    dice_sound()
                    draw_text(str(sorted_initiatives[selected_enemy][1].name) + ' takes ' + str(damage) + ' damage!', font, text_col, log_x, log_y + 60, screen)
                    sorted_initiatives[selected_enemy][1].take_damage(damage)

                    if sorted_initiatives[selected_enemy][1].alive:
                        draw_text(str(sorted_initiatives[selected_enemy][1].name) + ' has ' + str(sorted_initiatives[selected_enemy][1].hp) + ' left', font, text_col, log_x, log_y + 90, screen)
                        pygame.display.update()
                        pygame.time.wait(2500)
                        
                    else:
                        draw_text(str(sorted_initiatives[selected_enemy][1].name) + ' falls!', font, text_col, log_x, log_y + 90, screen)
                            
                        if player.race == 'human':
                            draw_text('You gain ' + str(int(1.1*sorted_initiatives[selected_enemy][1].xp)) + ' xp!', font, text_col, log_x, log_y + 120, screen)
                            player.xp += int(1.1*sorted_initiatives[selected_enemy][1].xp)
                        else:
                            draw_text('You gain ' + str(int(sorted_initiatives[selected_enemy][1].xp)) + ' xp!', font, text_col, log_x, log_y + 120, screen)
                            player.xp += int(sorted_initiatives[selected_enemy][1].xp)
                        pygame.display.update()
                        pygame.time.wait(2500)
                        sorted_initiatives.pop(selected_enemy)

                else:
                    draw_text('Attack roll: ' + str(attack_roll) + ' vs. ' + str(sorted_initiatives[selected_enemy][1].ac) + 'AC', font, text_col, log_x, log_y, screen)
                    draw_text('You miss!',font, text_col, log_x, log_y + 30, screen)
                    pygame.display.update()
                    pygame.time.wait(2500)
                    
                sorted_initiatives.append(sorted_initiatives.pop(0))

            elif selected_spell:
                spell.spell_function(player, sorted_initiatives, selected_enemy, font, text_col, log_x, log_y, screen)




        #Enemy turn
            
        else:
            enemy = sorted_initiatives[0][1]

            dice_sound()
            attack_roll, crit = enemy.weapon.attack_roll(enemy)

            if attack_roll >= player.ac():

                draw_text('Attack roll: ' + str(attack_roll) + ' vs. ' + str(player.ac()) + 'AC', font, text_col, log_x, log_y, screen)
                draw_text(enemy.name + ' hits you!', font, text_col, log_x, log_y + 30, screen)
                pygame.display.update()
                pygame.time.wait(2500)

                damage = enemy.weapon.damage_roll(enemy, crit)
                dice_sound()
                draw_text(enemy.name + ' deals ' + str(damage) + ' damage!', font, text_col, log_x, log_y + 60, screen)
                player.take_damage(damage)

                if player.alive:
                    draw_text('You withstand the attack!', font, text_col, log_x, log_y + 90, screen)
                    pygame.display.update()
                    pygame.time.wait(2500)
                    
                else:
                    draw_text('YOU DIED!', font, text_col, log_x, log_y + 90, screen)
                    pygame.display.update()
                    pygame.time.wait(2500)

            else:
                draw_text('Attack roll: ' + str(attack_roll) +     ' vs.' + str(player.ac()) + 'AC', font, text_col, log_x, log_y, screen)
                draw_text(enemy.name + ' missed you!',font, text_col, log_x, log_y + 30, screen)
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
        mana_bar(player, 20, 70, (255,255,255), screen)

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
            old_mp = player.max_mp
            animation = True

            if player.dnd_class == 'fighter':
                draw_text('HP: ' + str(player.max_hp) + ' ->' + ' ' + str(player.max_hp + 6 + int(stat_modifier[player.con])), font, color, 100, 200, screen)
                player.max_hp+=(6+ int(stat_modifier[player.con]))
                player.hp+=(6+ int(stat_modifier[player.con]))
                player.lvl = 2
                pygame.display.update()
                clock.tick(60)
                pygame.time.wait(1000)
            elif player.dnd_class == 'wizard':
                draw_text('HP: ' + str(player.max_hp) + ' ->' + ' ' + str(player.max_hp + 4 + int(stat_modifier[player.con])), font, color, 100, 200, screen)
                player.max_hp+=(4+ int(stat_modifier[player.con]))
                player.hp+=(4+ int(stat_modifier[player.con]))
                player.lvl = 2
                pygame.display.update()
                clock.tick(60)
                pygame.time.wait(1000)

            draw_text('MP: ' + str(player.max_mp), font, color, 100, 300, screen)
            pygame.display.update()
            clock.tick(60)
            pygame.time.wait(1000)

            draw_text('MP: ' + str(player.max_mp) + ' ->', font, color, 100, 300, screen)
            pygame.display.update()
            clock.tick(60)
            pygame.time.wait(1000)

            if player.dnd_class == 'fighter':
                draw_text('MP: ' + str(player.max_mp) + ' ->' + ' ' + str(player.max_mp + 2 + int(stat_modifier[player.wis])), font, color, 100, 300, screen)
                player.max_mp+=(2+ int(stat_modifier[player.wis]))
                player.mp+=(2+ int(stat_modifier[player.wis]))
                pygame.display.update()
                clock.tick(60)
                pygame.time.wait(1000)
            elif player.dnd_class == 'wizard':
                draw_text('MP: ' + str(player.max_mp) + ' ->' + ' ' + str(player.max_mp + 5 + int(stat_modifier[player.wis])), font, color, 100, 300, screen)
                player.max_mp+=(5+ int(stat_modifier[player.wis]))
                player.mp+=(5+ int(stat_modifier[player.wis]))
                pygame.display.update()
                clock.tick(60)
                pygame.time.wait(1000)

        draw_text('HP: ' + str(old_hp) + ' ->' + ' ' + str(player.max_hp), font, color, 100, 200, screen)
        draw_text('MP: ' + str(old_mp) + ' ->' + ' ' + str(player.max_mp), font, color, 100, 300, screen)

        if continue_button.draw(screen):
            quitting = True


        pygame.display.update()
        clock.tick(60)

def loot_menu(player, difficulty, screen, clock):

    looting = True
    quitting = False

    continue_img = pygame.image.load('Pictures/continue.png').convert_alpha()
    continue_button = button.ButtonSlow(600, 600, continue_img, 0.3)

    log_x = 20
    log_y = 100

    LOOT = []

    if difficulty == 1:

        gold = 20
        
        percent1 = np.random.randint(1,101)
        if percent1 > 20:
            loot = equipment.LOOT1[np.random.randint(len(equipment.LOOT1))]
            if loot.name == 'gold':
                gold += loot.value
            else:
                LOOT.append(loot)
        
        percent2 = np.random.randint(1,101)
        if percent2 > 80:
            loot = equipment.LOOT1[np.random.randint(len(equipment.LOOT1))]
            if loot.name == 'gold':
                gold += loot.value
            else:
                LOOT.append(loot)
        
        LOOT.append(equipment.Item('gold', gold))

    elif difficulty == 4:

        gold = 50

        percent1 = np.random.randint(1,101)
        if percent1 > 20:
            loot = equipment.LOOT4[np.random.randint(len(equipment.LOOT4))]
            if loot.name == 'gold':
                gold += loot.value
            else:
                LOOT.append(loot)
        
        percent2 = np.random.randint(1,101)
        if percent2 > 20:
            loot = equipment.LOOT4[np.random.randint(len(equipment.LOOT4))]
            if loot.name == 'gold':
                gold += loot.value
            else:
                LOOT.append(loot)

        percent3 = np.random.randint(1,101)
        if percent3 > 80:
            loot = equipment.LOOT1[np.random.randint(len(equipment.LOOT1))]
            if loot.name == 'gold':
                gold += loot.value
            else:
                LOOT.append(loot)

        percent4 = np.random.randint(1,101)
        if percent4 > 50:
            loot = equipment.LOOT1[np.random.randint(len(equipment.LOOT1))]
            if loot.name == 'gold':
                gold += loot.value
            else:
                LOOT.append(loot)

        LOOT.append(equipment.Item('gold', gold))

    BUTTONS = []
    x = 300
    y = 100
    dy = 0
    for loot in LOOT:
        buttonq = loot.get_ButtonOnce(player, x, y+dy, 1)
        dy += 50
        BUTTONS.append(buttonq)



    while looting and not quitting:

        for event in pygame.event.get():
            #Quit check
            if event.type == pygame.QUIT:
                run = False
                quitting = True

        screen.fill((229,203,186))

        draw_text('LOOT!', pygame.font.SysFont(None, 50), (0,0,0), 500, 30, screen)
        
        health_bar(player, 20, 20, 0, (255,255,255), screen)
        xp_bar(player, 20, 20, (255,255,255), screen)
        mana_bar(player, 20, 70, (255,255,255), screen)
        draw_text('AC: ' + str(player.ac()), pygame.font.SysFont(None, 40), (0,0,0), 50, 260, screen)
        draw_text('Gold: ' + str(player.gold), pygame.font.SysFont(None, 30), (0,0,0), 50, 300, screen)
        draw_text('Inventory slots: ' + str(len(player.inventory)) + '/' + str(player.inventory_size), pygame.font.SysFont(None, 30), (0,0,0), 50, 320, screen)
        draw_text('Current equipment:', pygame.font.SysFont(None, 30), (0,0,0), 50, 340, screen)

        dy = 20
        j=1
        if player.right_hand != None:
            draw_text(player.right_hand.name, pygame.font.SysFont(None, 30), (0,0,0), 50, 340 + j*dy, screen)
            j+=1
            
        if player.left_hand != None:
            draw_text(player.left_hand.name, pygame.font.SysFont(None, 30), (0,0,0), 50, 340 + j*dy, screen)
            j+=1

        if player.armor != None:
            draw_text(player.armor.name, pygame.font.SysFont(None, 30), (0,0,0), 50, 340 + j*dy, screen)
            j+=1

        for item in player.inventory:
            draw_text(item.name, pygame.font.SysFont(None, 30), (0,0,0), 50, 340 + j*dy, screen)
            j+=1

        i=0
        while i<len(BUTTONS):
            if BUTTONS[i].draw(screen):
                if LOOT[i].name == 'gold':
                    player.gold += LOOT[i].value
                else:
                    if len(player.inventory) <= player.inventory_size:
                        player.inventory.append(LOOT[i])
                    else:
                        draw_text('Your inventory is full! (work in progress)', pygame.font.SysFont(None, 30), (0,0,0), 700, 500, screen)
            i+=1

        if continue_button.draw(screen):
            looting = False

        pygame.display.update()
        clock.tick(60)

def inventory_menu(player, screen, clock, SCREEN_WIDTH, SCREEN_HEIGHT):

    scale = 1000/SCREEN_WIDTH
    inventorying = True
    quitting = False

    TH_weapon_selected = False
    OH_weapon_selected = False
    armor_selected = False
    shield_selected = False

    #Left hand inventory slot
    lhand_x = 300
    lhand_y = 70
    lhand_rect = pygame.Rect(scale*(lhand_x), scale*(lhand_y), 200, 130)
    lhand_selected_rect = pygame.Rect(scale*(lhand_x - 10), scale*(lhand_y), 250, 162.5)
    lhand_text = pygame.font.SysFont(None, 40).render('LEFT HAND', True, (0,0,0))

    #Right hand inventory slot
    rhand_x = lhand_x + 220
    rhand_y = 70
    rhand_rect = pygame.Rect(scale*(rhand_x), scale*(rhand_y), 200, 130)
    rhand_selected_rect = pygame.Rect(scale*(rhand_x - 10), scale*(rhand_y), 250, 162.5)
    rhand_text = pygame.font.SysFont(None, 40).render('RIGHT HAND', True, (0,0,0))

    #Armor inventory slot
    armor_x = rhand_x + 220
    armor_y = 70
    armor_rect = pygame.Rect(scale*(armor_x), scale*(armor_y), 200, 130)
    armor_selected_rect = pygame.Rect(scale*(armor_x), scale*(armor_y), 250, 162.5)
    armor_text = pygame.font.SysFont(None, 40).render('ARMOR', True, (0,0,0))

    while inventorying and not quitting:

        for event in pygame.event.get():
            #Quit check
            if event.type == pygame.QUIT:
                quitting = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    inventorying = False

        mouse_x, mouse_y = pygame.mouse.get_pos()

        screen.fill((229,203,186))
        health_bar(player, scale*20, scale*20, 0, (255,255,255), screen)
        xp_bar(player, scale*20, scale*20, (255,255,255), screen)
        mana_bar(player, scale*20, scale*70, (255,255,255), screen)
        draw_text('Equipped', pygame.font.SysFont(None, 50), (0,0,0), 500, 30, screen)

        #TODO: Draw spells starting from around y=250 and x=700 (like a one column list on the right side of the screen)

        #Draw equippable slots differently depending on which item is currently held
        if TH_weapon_selected == False and OH_weapon_selected == False and armor_selected == False and shield_selected == False:

            #Draw inventory slots
            i=0
            j=0
            x=50
            y=580
            dx = 20
            dy = 80

            draw_text('Inventory', pygame.font.SysFont(None, 50), (0,0,0), x, y-40, screen)

            while i<12:
                if i<player.inventory_size:
                    pygame.draw.rect(screen, (74,5,44), pygame.Rect(scale*(x + j*(150+dx)), scale*y, 150,50), width=4)

                    #Draw inventory button
                    if i<len(player.inventory):
                        item = player.inventory[i]
                        img_width, img_height = item.get_ButtonOnceLR(player, scale*(x + j*(150+dx)), scale*y, 1, just_dimensions=True)
                        rescale = find_scale_factor(150 - 8, 50 - 8, img_width, img_height)
                        button = item.get_ButtonOnceLR(player, scale*(x + j*(150+dx)) + 4, scale*y + 4, rescale)
                        button_return = button.draw(screen)
                        if button_return == True:
                            if isinstance(item, equipment.Armor):
                                armor_selected = True
                                skip_index = i
                                selected_item = item
                                break
                            elif isinstance(item, equipment.Weapon):
                                if item.two_handed:
                                    TH_weapon_selected = True
                                else:
                                    OH_weapon_selected = True
                                skip_index = i
                                selected_item = item
                                break
                            elif isinstance(item, equipment.Shield):
                                shield_selected = True
                                skip_index = i
                                selected_item = item
                                break
                        elif button_return == 2:
                            player.inventory.pop(i)

                    j+=1

                    if j == 4:
                        y+=dy
                        j=0

                else:
                    pygame.draw.rect(screen, (138,138,138), pygame.Rect(scale*(x + j*(150+dx)), scale*y, 150,50), width=0)
                    j+=1

                    if j == 4:
                        y+=dy
                        j=0

                i+=1
            
            #left hand            
            pygame.draw.rect(screen, (74,5,44), lhand_rect, width=5)
            screen.blit(lhand_text, (scale*(lhand_x+5), scale*(lhand_y + 5)))
            if player.left_hand != None:
                img_width, img_height = player.left_hand.get_ButtonOnceLR(player, scale*(lhand_x + 5), scale*(lhand_y + 5), 1, just_dimensions=True)
                rescale = find_scale_factor(200 - 10, 130 - 10 - 30, img_width, img_height)
                button_lhand = player.left_hand.get_ButtonOnceLR(player, scale*(lhand_x + 5), scale*(lhand_y + 5 + 30), rescale)
                if button_lhand.draw(screen):
                    if len(player.inventory)<player.inventory_size:
                        player.inventory.append(player.left_hand)
                        player.left_hand = None
                        pygame.mouse.set_pos([500,400])

            #right hand            
            pygame.draw.rect(screen, (74,5,44), rhand_rect, width=5)
            screen.blit(rhand_text, (scale*(rhand_x+5), scale*(rhand_y + 5)))
            if player.right_hand != None:
                img_width, img_height = player.right_hand.get_ButtonOnceLR(player, scale*(rhand_x + 5), scale*(rhand_y + 5), 1, just_dimensions=True)
                rescale = find_scale_factor(200 - 10, 130 - 10 - 30, img_width, img_height)
                button_rhand = player.right_hand.get_ButtonOnceLR(player, scale*(rhand_x + 5), scale*(rhand_y + 5 + 30), rescale)
                if button_rhand.draw(screen):
                    if len(player.inventory)<player.inventory_size:
                        player.inventory.append(player.right_hand)
                        player.right_hand = None
                        pygame.mouse.set_pos([500,400])


            #armor            
            pygame.draw.rect(screen, (74,5,44), armor_rect, width=5)
            screen.blit(armor_text, (scale*(armor_x+5), scale*(armor_y + 5)))
            if player.armor != None:
                img_width, img_height = player.armor.get_ButtonOnceLR(player, scale*(armor_x + 5), scale*(armor_y + 5), 1, just_dimensions=True)
                rescale = find_scale_factor(200 - 10, 130 - 10 - 30, img_width, img_height)
                button_armor = player.armor.get_ButtonOnceLR(player, scale*(armor_x + 5), scale*(armor_y + 5 + 30), rescale)
                if button_armor.draw(screen):
                    if len(player.inventory)<player.inventory_size:
                        player.inventory.append(player.armor)
                        player.armor = None
                        pygame.mouse.set_pos([500,400])

        #Armor is selected
        if armor_selected:

            big_button = selected_item.get_ButtonOnceLR(player, 50, 250, 3)
            if big_button.draw(screen):
                armor_selected = False

            #Draw inventory slots
            i=0
            j=0
            x=50
            y=580
            dx = 20
            dy = 80

            draw_text('Inventory', pygame.font.SysFont(None, 50), (0,0,0), x, y-40, screen)

            while i<12:
                if i<player.inventory_size:
                    pygame.draw.rect(screen, (74,5,44), pygame.Rect(scale*(x + j*(150+dx)), scale*y, 150,50), width=4)

                    #Draw inventory button
                    if i<len(player.inventory):
                        item = player.inventory[i]
                        img_width, img_height = item.get_ButtonOnceLR(player, scale*(x + j*(150+dx)), scale*y, 1, just_dimensions=True)
                        rescale = find_scale_factor(150 - 8, 50 - 8, img_width, img_height)
                        button = item.get_ButtonOnceLR(player, scale*(x + j*(150+dx)) + 4, scale*y + 4, rescale)
                        button_value = button.draw(screen)
                        if button_value == True:
                            if isinstance(item, equipment.Armor):
                                armor_selected = True
                                skip_index = i
                                selected_item = item
                                break
                            elif isinstance(item, equipment.Weapon):
                                if item.two_handed:
                                    TH_weapon_selected = True
                                else:
                                    OH_weapon_selected = True
                                armor_selected = False
                                skip_index = i
                                selected_item = item
                                break
                            elif isinstance(item, equipment.Shield):
                                shield_selected = True
                                armor_selected = False
                                skip_index = i
                                selected_item = item
                                break
                        elif button_value == 2:
                            player.inventory.pop(i)

                    j+=1

                    if j == 4:
                        y+=dy
                        j=0

                else:
                    pygame.draw.rect(screen, (138,138,138), pygame.Rect(scale*(x + j*(150+dx)), scale*y, 150,50), width=0)
                    j+=1

                    if j == 4:
                        y+=dy
                        j=0

                i+=1

            #left hand
            pygame.draw.rect(screen, (138,138,138), lhand_rect, width=0)
            screen.blit(lhand_text, (scale*(lhand_x+5), scale*(lhand_y + 5)))
            if player.left_hand != None:
                img_width, img_height = player.left_hand.get_ButtonOnceLR(player, scale*(lhand_x + 5), scale*(lhand_y + 5), 1, just_dimensions=True)
                rescale = find_scale_factor(200 - 10, 130 - 10 - 30, img_width, img_height)
                button_lhand = player.left_hand.get_ButtonOnceLR(player, scale*(lhand_x + 5), scale*(lhand_y + 5 + 30), rescale)
                button_lhand.clicked = True
                button_lhand.draw(screen)

            #right hand
            pygame.draw.rect(screen, (138,138,138), rhand_rect, width=0)
            screen.blit(rhand_text, (scale*(rhand_x+5), scale*(rhand_y + 5)))
            if player.right_hand != None:
                img_width, img_height = player.right_hand.get_ButtonOnceLR(player, scale*(rhand_x + 5), scale*(rhand_y + 5), 1, just_dimensions=True)
                rescale = find_scale_factor(200 - 10, 130 - 10 - 30, img_width, img_height)
                button_rhand = player.right_hand.get_ButtonOnceLR(player, scale*(rhand_x + 5), scale*(rhand_y + 5 + 30), rescale)
                button_rhand.clicked = True
                button_rhand.draw(screen)

            #armor
            pygame.draw.rect(screen, (74,5,44), armor_rect, width=8)
            screen.blit(armor_text, (scale*(armor_x+5), scale*(armor_y + 5)))
            if armor_rect.collidepoint(mouse_x, mouse_y):
                if pygame.mouse.get_pressed()[0] == 1:
                    pygame.mouse.set_pos([500,400])
                    current_armor = player.armor
                    if current_armor != None:
                        player.armor = selected_item
                        player.inventory.pop(skip_index)
                        player.inventory.append(current_armor)
                    else:
                        player.armor = selected_item
                        player.inventory.pop(skip_index)
                    armor_selected = False

        #Two-handed weapon is selected
        if TH_weapon_selected:

            big_button = selected_item.get_ButtonOnceLR(player, 50, 250, 3)
            if big_button.draw(screen):
                TH_weapon_selected = False

            #Draw inventory slots
            i=0
            j=0
            x=50
            y=580
            dx = 20
            dy = 80

            draw_text('Inventory', pygame.font.SysFont(None, 50), (0,0,0), x, y-40, screen)

            while i<12:
                if i<player.inventory_size:
                    pygame.draw.rect(screen, (74,5,44), pygame.Rect(scale*(x + j*(150+dx)), scale*y, 150,50), width=4)

                    #Draw inventory button
                    if i<len(player.inventory):
                        item = player.inventory[i]
                        img_width, img_height = item.get_ButtonOnceLR(player, scale*(x + j*(150+dx)), scale*y, 1, just_dimensions=True)
                        rescale = find_scale_factor(150 - 8, 50 - 8, img_width, img_height)
                        button = item.get_ButtonOnceLR(player, scale*(x + j*(150+dx)) + 4, scale*y + 4, rescale)
                        button_value = button.draw(screen)
                        if button_value == True:
                            if isinstance(item, equipment.Armor):
                                armor_selected = True
                                TH_weapon_selected = False
                                skip_index = i
                                selected_item = item
                                break
                            elif isinstance(item, equipment.Weapon):
                                if item.two_handed:
                                    TH_weapon_selected = True
                                else:
                                    OH_weapon_selected = True
                                    TH_weapon_selected = False
                                skip_index = i
                                selected_item = item
                                break
                            elif isinstance(item, equipment.Shield):
                                shield_selected = True
                                TH_weapon_selected = False
                                skip_index = i
                                selected_item = item
                                break
                        elif button_value == 2:
                            player.inventory.pop(i)

                    j+=1

                    if j == 4:
                        y+=dy
                        j=0

                else:
                    pygame.draw.rect(screen, (138,138,138), pygame.Rect(scale*(x + j*(150+dx)), scale*y, 150,50), width=0)
                    j+=1

                    if j == 4:
                        y+=dy
                        j=0

                i+=1

            #left hand
            pygame.draw.rect(screen, (138,138,138), lhand_rect, width=0)
            screen.blit(lhand_text, (scale*(lhand_x+5), scale*(lhand_y + 5)))
            if player.left_hand != None:
                img_width, img_height = player.left_hand.get_ButtonOnceLR(player, scale*(lhand_x + 5), scale*(lhand_y + 5), 1, just_dimensions=True)
                rescale = find_scale_factor(200 - 10, 130 - 10 - 30, img_width, img_height)
                button_lhand = player.left_hand.get_ButtonOnceLR(player, scale*(lhand_x + 5), scale*(lhand_y + 5 + 30), rescale)
                button_lhand.clicked = True
                button_lhand.draw(screen)

            #right hand
            pygame.draw.rect(screen, (74,5,44), rhand_rect, width=8)
            screen.blit(rhand_text, (scale*(rhand_x+5), scale*(rhand_y + 5)))
            if rhand_selected_rect.collidepoint(mouse_x, mouse_y):
                if pygame.mouse.get_pressed()[0] == 1:
                    pygame.mouse.set_pos([500,400])
                    current_weapon = player.right_hand
                    if current_weapon != None:
                        player.right_hand = selected_item
                        player.inventory.pop(skip_index)
                        player.inventory.append(current_weapon)
                    else:
                        player.right_hand = selected_item
                        player.inventory.pop(skip_index)

                    if player.left_hand != None:
                        player.inventory.append(player.left_hand)
                        player.left_hand = None
                    
                    TH_weapon_selected = False

            #armor
            pygame.draw.rect(screen, (138,138,138), armor_rect, width=0)
            screen.blit(lhand_text, (scale*(lhand_x+5), scale*(lhand_y + 5)))
            if player.armor != None:
                img_width, img_height = player.armor.get_ButtonOnceLR(player, scale*(armor_x + 5), scale*(armor_y + 5), 1, just_dimensions=True)
                rescale = find_scale_factor(200 - 10, 130 - 10 - 30, img_width, img_height)
                button_armor = player.armor.get_ButtonOnceLR(player, scale*(armor_x + 5), scale*(armor_y + 5 + 30), rescale)
                button_armor.clicked = True
                button_armor.draw(screen)

        #One-handed weapon selected
        if OH_weapon_selected:
            big_button = selected_item.get_ButtonOnceLR(player, 50, 250, 3)
            if big_button.draw(screen):
                OH_weapon_selected = False

            #Draw inventory slots
            i=0
            j=0
            x=50
            y=580
            dx = 20
            dy = 80

            draw_text('Inventory', pygame.font.SysFont(None, 50), (0,0,0), x, y-40, screen)

            while i<12:
                if i<player.inventory_size:
                    pygame.draw.rect(screen, (74,5,44), pygame.Rect(scale*(x + j*(150+dx)), scale*y, 150,50), width=4)

                    #Draw inventory button
                    if i<len(player.inventory):
                        item = player.inventory[i]
                        img_width, img_height = item.get_ButtonOnceLR(player, scale*(x + j*(150+dx)), scale*y, 1, just_dimensions=True)
                        rescale = find_scale_factor(150 - 8, 50 - 8, img_width, img_height)
                        button = item.get_ButtonOnceLR(player, scale*(x + j*(150+dx)) + 4, scale*y + 4, rescale)
                        button_value = button.draw(screen)
                        if button_value:
                            if isinstance(item, equipment.Armor):
                                armor_selected = True
                                OH_weapon_selected = False
                                skip_index = i
                                selected_item = item
                                break
                            elif isinstance(item, equipment.Weapon):
                                if item.two_handed:
                                    TH_weapon_selected = True
                                    OH_weapon_selected = False
                                else:
                                    OH_weapon_selected = True
                                skip_index = i
                                selected_item = item
                                break
                            elif isinstance(item, equipment.Shield):
                                shield_selected = True
                                OH_weapon_selected = False
                                skip_index = i
                                selected_item = item
                                break
                        elif button_value == 2:
                            player.inventory.pop(i)

                    j+=1

                    if j == 4:
                        y+=dy
                        j=0

                else:
                    pygame.draw.rect(screen, (138,138,138), pygame.Rect(scale*(x + j*(150+dx)), scale*y, 150,50), width=0)
                    j+=1

                    if j == 4:
                        y+=dy
                        j=0

                i+=1

            #left hand
            pygame.draw.rect(screen, (74,5,44), lhand_rect, width=8)
            screen.blit(lhand_text, (scale*(lhand_x+5), scale*(lhand_y + 5)))
            if lhand_rect.collidepoint(mouse_x, mouse_y):
                if pygame.mouse.get_pressed()[0] == 1:
                    pygame.mouse.set_pos([500,400])
                    current_weapon = player.left_hand
                    if current_weapon != None:
                        player.left_hand = selected_item
                        player.inventory.pop(skip_index)
                        player.inventory.append(current_weapon)
                    else:
                        player.left_hand = selected_item
                        player.inventory.pop(skip_index)

                    if player.right_hand!=None:
                        if player.right_hand.two_handed:
                            player.inventory.append(player.right_hand)
                            player.right_hand = None
                    
                    OH_weapon_selected = False

            #right hand
            pygame.draw.rect(screen, (74,5,44), rhand_rect, width=8)
            screen.blit(rhand_text, (scale*(rhand_x+5), scale*(rhand_y + 5)))
            if rhand_rect.collidepoint(mouse_x, mouse_y):
                if pygame.mouse.get_pressed()[0] == 1:
                    pygame.mouse.set_pos([500,400])
                    current_weapon = player.right_hand
                    if current_weapon != None:
                        player.right_hand = selected_item
                        player.inventory.pop(skip_index)
                        player.inventory.append(current_weapon)
                    else:
                        player.right_hand = selected_item
                        player.inventory.pop(skip_index)
                    
                    OH_weapon_selected = False

            #armor
            pygame.draw.rect(screen, (138,138,138), armor_rect, width=0)
            screen.blit(lhand_text, (scale*(lhand_x+5), scale*(lhand_y + 5)))
            if player.armor != None:
                img_width, img_height = player.armor.get_ButtonOnceLR(player, scale*(armor_x + 5), scale*(armor_y + 5), 1, just_dimensions=True)
                rescale = find_scale_factor(200 - 10, 130 - 10 - 30, img_width, img_height)
                button_armor = player.armor.get_ButtonOnceLR(player, scale*(armor_x + 5), scale*(armor_y + 5 + 30), rescale)
                button_armor.clicked = True
                button_armor.draw(screen)
            
        #Shield selected
        if shield_selected:
            big_button = selected_item.get_ButtonOnceLR(player, 50, 250, 3)
            if big_button.draw(screen):
                TH_weapon_selected = False

            #Draw inventory slots
            i=0
            j=0
            x=50
            y=580
            dx = 20
            dy = 80

            draw_text('Inventory', pygame.font.SysFont(None, 50), (0,0,0), x, y-40, screen)

            while i<12:
                if i<player.inventory_size:
                    pygame.draw.rect(screen, (74,5,44), pygame.Rect(scale*(x + j*(150+dx)), scale*y, 150,50), width=4)

                    #Draw inventory button
                    if i<len(player.inventory):
                        item = player.inventory[i]
                        img_width, img_height = item.get_ButtonOnceLR(player, scale*(x + j*(150+dx)), scale*y, 1, just_dimensions=True)
                        rescale = find_scale_factor(150 - 8, 50 - 8, img_width, img_height)
                        button = item.get_ButtonOnceLR(player, scale*(x + j*(150+dx)) + 4, scale*y + 4, rescale)
                        button_value = button.draw(screen)
                        if button_value == True:
                            if isinstance(item, equipment.Armor):
                                armor_selected = True
                                shield_selected = False
                                skip_index = i
                                selected_item = item
                                break
                            elif isinstance(item, equipment.Weapon):
                                if item.two_handed:
                                    TH_weapon_selected = True
                                    shield_selected = False
                                else:
                                    OH_weapon_selected = True
                                    shield_selected = False
                                skip_index = i
                                selected_item = item
                                break
                            elif isinstance(item, equipment.Shield):
                                shield_selected = True
                                skip_index = i
                                selected_item = item
                                break
                        elif button_value == 2:
                            player.inventory.pop(i)

                    j+=1

                    if j == 4:
                        y+=dy
                        j=0

                else:
                    pygame.draw.rect(screen, (138,138,138), pygame.Rect(scale*(x + j*(150+dx)), scale*y, 150,50), width=0)
                    j+=1

                    if j == 4:
                        y+=dy
                        j=0

                i+=1

            #left hand
            pygame.draw.rect(screen, (74,5,44), lhand_rect, width=8)
            screen.blit(lhand_text, (scale*(lhand_x+5), scale*(lhand_y + 5)))
            if lhand_rect.collidepoint(mouse_x, mouse_y):
                if pygame.mouse.get_pressed()[0] == 1:
                    pygame.mouse.set_pos([500,400])
                    current_weapon = player.left_hand
                    if current_weapon != None:
                        player.left_hand = selected_item
                        player.inventory.pop(skip_index)
                        player.inventory.append(current_weapon)
                    else:
                        player.left_hand = selected_item
                        player.inventory.pop(skip_index)
                    
                    shield_selected = False

            #right hand
            pygame.draw.rect(screen, (138,138,138), rhand_rect, width=0)
            screen.blit(rhand_text, (scale*(rhand_x+5), scale*(rhand_y + 5)))
            if player.right_hand != None:
                img_width, img_height = player.right_hand.get_ButtonOnceLR(player, scale*(rhand_x + 5), scale*(rhand_y + 5), 1, just_dimensions=True)
                rescale = find_scale_factor(200 - 10, 130 - 10 - 30, img_width, img_height)
                button_rhand = player.right_hand.get_ButtonOnceLR(player, scale*(rhand_x + 5), scale*(rhand_y + 5 + 30), rescale)
                button_rhand.clicked = True
                button_rhand.draw(screen)

            #armor
            pygame.draw.rect(screen, (138,138,138), armor_rect, width=0)
            screen.blit(armor_text, (scale*(armor_x+5), scale*(armor_y + 5)))
            if player.armor != None:
                img_width, img_height = player.armor.get_ButtonOnceLR(player, scale*(armor_x + 5), scale*(armor_y + 5), 1, just_dimensions=True)
                rescale = find_scale_factor(200 - 10, 130 - 10 - 30, img_width, img_height)
                button_armor = player.armor.get_ButtonOnceLR(player, scale*(armor_x + 5), scale*(armor_y + 5 + 30), rescale)
                button_armor.clicked = True
                button_armor.draw(screen)
        
        pygame.display.update()
        clock.tick(60)


def find_scale_factor(rect_width, rect_height, img_width, img_height):
    scale_width = rect_width/img_width
    scale_height = rect_height/img_height

    scale_factor = min(scale_width, scale_height)

    return scale_factor




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

def mana_bar(player, x, y, col, screen):

    mana_font = pygame.font.SysFont(None, 30)
    background_width = 45 + player.mp*2
    active_width = background_width*(player.mp/player.max_mp)

    pygame.draw.rect(screen, (0,0,0), (x, y, background_width, 25))
    pygame.draw.rect(screen, (11,20,143),(x+1, y+1, active_width, 23))
    draw_text(str(player.mp) + '/' + str(player.max_mp), mana_font, col, x+2, y+3, screen)



# ------------------------------------------------------------------------------------------------------------------------------------------------
# SPECIAL ENCOUNTERS
# ------------------------------------------------------------------------------------------------------------------------------------------------


