#Import section
import pygame
import button
import functions
import equipment
import creatures
import encounters
import dungeons
import spellbook
pygame.init()

#Screen setup
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Goofy ahh RPG')

clock = pygame.time.Clock()

# GLOBAL Buttons
start_img = pygame.image.load('Pictures/start.png').convert_alpha()
pause_img = pygame.image.load('Pictures/pause.png').convert_alpha()
quit_img = pygame.image.load('Pictures/quit.png').convert_alpha()
resume_img = pygame.image.load('Pictures/resume.png').convert_alpha()
plus_img = pygame.image.load('Pictures/plus.png').convert_alpha()
minus_img = pygame.image.load('Pictures/minus.png').convert_alpha()

lvlup_icon_img = pygame.image.load('Pictures/levelup_icon.png').convert_alpha()


start_button = button.ButtonSlow(100,200, start_img, 0.4)
pause_button = button.ButtonSlow(10, 10, pause_img, 0.2)
resume_button = button.ButtonSlow(100, 200, resume_img, 0.4)
quit_button = button.Button(100, 400, quit_img, 0.4)

lvlup_icon_button = button.ButtonSlow(230, 20, lvlup_icon_img, 0.19)

#STAT SELECT --------------------------------------------------------------------------------------------------------------

#Images
race_img = pygame.image.load('Pictures/race.png').convert_alpha()
back_img = pygame.image.load('Pictures/back.png').convert_alpha()

#Buttons
str_up = button.Button(700, 100, plus_img, 0.5)
dex_up = button.Button(700, 200, plus_img, 0.5)
con_up = button.Button(700, 300, plus_img, 0.5)
int_up = button.Button(700, 400, plus_img, 0.5)
wis_up = button.Button(700, 500, plus_img, 0.5)
cha_up = button.Button(700, 600, plus_img, 0.5)
str_down = button.Button(200, 100, minus_img, 0.5)
dex_down = button.Button(200, 200, minus_img, 0.5)
con_down = button.Button(200, 300, minus_img, 0.5)
int_down = button.Button(200, 400, minus_img, 0.5)
wis_down = button.Button(200, 500, minus_img, 0.5)
cha_down = button.Button(200, 600, minus_img, 0.5)

race_button = button.ButtonSlow(750, 710, race_img, 0.3)
back_button = button.ButtonSlow(20, 710, back_img, 0.3)

orc_selected = False
elf_selected = False
human_selected = False

#RACE SELECT --------------------------------------------------------------------------------------------------------------

#Images
human_img = pygame.image.load('Pictures/human.png').convert_alpha()
orc_img = pygame.image.load('Pictures/orc.png').convert_alpha()
elf_img = pygame.image.load('Pictures/elf.png').convert_alpha()
human_selected_img = pygame.image.load('Pictures/human_selected.png').convert_alpha()
orc_selected_img = pygame.image.load('Pictures/orc_selected.png').convert_alpha()
elf_selected_img = pygame.image.load('Pictures/elf_selected.png').convert_alpha()

class_img = pygame.image.load('Pictures/class.png').convert_alpha()

#Buttons
orc_button = button.ButtonSlow(650, 100, orc_img, 0.4)
orc_button_pressed = button.ButtonSlow(650, 100, orc_selected_img, 0.4)
elf_button = button.ButtonSlow(650, 300, elf_img, 0.4)
elf_button_pressed = button.ButtonSlow(650, 300, elf_selected_img, 0.4)
human_button = button.ButtonSlow(650, 500, human_img, 0.4)
human_button_pressed = button.ButtonSlow(650, 500, human_selected_img, 0.4)

class_button = button.ButtonSlow(750, 710, class_img, 0.3)

#CLASS SELECT --------------------------------------------------------------------------------------------------------------

#Images
fighter_img = pygame.image.load('Pictures/fighter.png').convert_alpha()
fighter_selected_img = pygame.image.load('Pictures/fighter_selected.png').convert_alpha()
wizard_img = pygame.image.load('Pictures/wizard.png').convert_alpha()
wizard_selected_img = pygame.image.load('Pictures/wizard_selected.png').convert_alpha()

#Buttons
fighter_button = button.ButtonSlow(700, 30, fighter_img, 0.4)
fighter_selected_button = button.ButtonSlow(700,30,fighter_selected_img, 0.4)
wizard_button = button.ButtonSlow(700, 130, wizard_img, 0.4)
wizard_selected_button = button.ButtonSlow(700,130,wizard_selected_img,0.4)

#EQUIPMENT SELECT --------------------------------------------------------------------------------------------------------------

#Images
equipment_img = pygame.image.load('Pictures/equipment.png').convert_alpha()
longsword_img = pygame.image.load('Pictures/longsword.png').convert_alpha()
longsword_selected_img = pygame.image.load('Pictures/longsword_selected.png').convert_alpha()
longbow_img = pygame.image.load('Pictures/longbow.png').convert_alpha()
longbow_selected_img = pygame.image.load('Pictures/longbow_selected.png').convert_alpha()

firebolt_img = pygame.image.load('Pictures/firebolt.png').convert_alpha()
firebolt_selected_img = pygame.image.load('Pictures/firebolt_selected.png').convert_alpha()

adventure_img = pygame.image.load('Pictures/adventure.png').convert_alpha()

god_mode_img = pygame.image.load('Pictures/god_mode.png').convert_alpha()
god_mode_selected_img = pygame.image.load('Pictures/god_mode_selected.png').convert_alpha()


#Buttons
equipment_button = button.ButtonSlow(720, 690, equipment_img, 0.3)
longsword_button = button.ButtonSlow(500, 100, longsword_img, 0.4)
longsword_selected_button = button.ButtonSlow(500, 100, longsword_selected_img, 0.4)
longbow_button = button.ButtonSlow(500, 500, longbow_img, 0.4)
longbow_selected_button = button.ButtonSlow(500, 500, longbow_selected_img, 0.4)

firebolt_button = button.ButtonSlow(500, 100, firebolt_img, 0.4)
firebolt_selected_button = button.ButtonSlow(500, 100, firebolt_selected_img, 0.4)

adventure_button = button.ButtonSlow(710, 690, adventure_img, 0.25)

god_mode_button = button.ButtonSlow(100, 600, god_mode_img, 0.3)
god_mode_selected_button = button.ButtonSlow(100, 600, god_mode_selected_img, 0.3)

#CHAPTER 1 --------------------------------------------------------------------------------------------------------------

#Images
fight_img = pygame.image.load('Pictures/fight.png').convert_alpha()
dungeon_img = pygame.image.load('Pictures/dungeon.png').convert_alpha()

#Buttons
fight_button1 = button.ButtonSlow(40, 650, fight_img, 0.3)
fight_button2 = button.ButtonSlow(340, 650, fight_img, 0.3)
fight_button3 = button.ButtonSlow(640, 650, fight_img, 0.3)
dungeon_button = button.ButtonSlow(340, 650, dungeon_img, 0.3)





#variables
P_EQUIPMENT = []
shield = False
arrows = 0



#additional objects setup
font = pygame.font.SysFont(None,40)
stat_font = pygame.font.SysFont(None, 30)
text_col = (0,0,0)

"""
#Function to draw text on screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))
"""



#Dictionary of point costs for stats
point_cost = {9:1, 10:1, 11:1, 12:1, 13:1, 14:2, 15:2}
point_gain = {14:2, 13:2, 12:1, 11:1, 10:1, 9:1, 8:1}
stat_modifier = {1:'-5', 2:'-4', 3:'-4', 4:'-3', 5:'-3', 6:'-2', 7:'-2', 8:'-1', 9:'-1', 10:'+0', 11:'+0', 12:'+1', 13:'+1', 14:'+2', 15:'+2', 16:'+3', 17:'+3', 18:'+4', 19:'+4', 20:'+5', 21:'+5', 22:'+6', 23:'+6', 24:'+7', 25:'+7'}



start_menu = True
run = True

#variables




while run:

#START MENU --------------------------------------------------------------------------------------------------------------
    


    while start_menu and run:
        pygame.mixer.music.load('Sounds/character_bg.mp3')
        pygame.mixer.music.play(-1)

        #Game Segment Booleans
        game_paused = False
        stat_select = False
        race_select = False
        class_select = False
        equipment_select = False

        god_mode = False

        adventure1 = False
        dungeon1 = False
        dungeon2 = False


        STATS = [8,8,8,8,8,8]
        player = creatures.Player()
        player.inventory = []
        points = 27

        screen.fill((229,203,186))

        if start_button.draw(screen):
            stat_select = True
            start_menu = False
        if quit_button.draw(screen):
            run = False

        for event in pygame.event.get():
            #Quit check
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(60)

#STAT SELECT --------------------------------------------------------------------------------------------------------------

    if not start_menu:
        # DUNGEONS --------------------------------------------------------------------------------------------------------------
        DUNGEON_IMGS = [pygame.image.load('Dungeons/intro_dungeon.jpg').convert_alpha()]
        DUNGEONS = [dungeons.Dungeon(DUNGEON_IMGS[0], 340, 100, 0.25, dungeons.EVENT_POS[0])]

    while stat_select and run:

        screen.fill((229,203,186))

        #Game Started
        if not game_paused:

            #Pause button
            if pause_button.draw(screen):
                game_paused = True

            #Stat print
            functions.draw_text('Points left: ' + str(points), font, text_col, 200, 50, screen)
            functions.draw_stats(STATS, stat_modifier, font, text_col, 400, 150, 100, screen)
            #Stat buying
            if str_up.draw(screen) and STATS[0]<15 and point_cost[STATS[0]+1]<=points:
                STATS[0]+=1
                points-=point_cost[STATS[0]]
            if dex_up.draw(screen) and STATS[1]<15 and point_cost[STATS[1]+1]<=points:
                STATS[1]+=1
                points-=point_cost[STATS[1]]
            if con_up.draw(screen) and STATS[2]<15 and point_cost[STATS[2]+1]<=points:
                STATS[2]+=1
                points-=point_cost[STATS[2]]
            if int_up.draw(screen) and STATS[3]<15 and point_cost[STATS[3]+1]<=points:
                STATS[3]+=1
                points-=point_cost[STATS[3]]
            if wis_up.draw(screen) and STATS[4]<15 and point_cost[STATS[4]+1]<=points:
                STATS[4]+=1
                points-=point_cost[STATS[4]]
            if cha_up.draw(screen) and STATS[5]<15 and point_cost[STATS[5]+1]<=points:
                STATS[5]+=1
                points-=point_cost[STATS[5]]
            #Stat selling
            if str_down.draw(screen) and STATS[0]>8:
                STATS[0]-=1
                points+=point_gain[STATS[0]]
            if dex_down.draw(screen) and STATS[1]>8:
                STATS[1]-=1
                points+=point_gain[STATS[1]]
            if con_down.draw(screen) and STATS[2]>8:
                STATS[2]-=1
                points+=point_gain[STATS[2]]
            if int_down.draw(screen) and STATS[3]>8:
                STATS[3]-=1
                points+=point_gain[STATS[3]]
            if wis_down.draw(screen) and STATS[4]>8:
                STATS[4]-=1
                points+=point_gain[STATS[4]]
            if cha_down.draw(screen) and STATS[5]>8:
                STATS[5]-=1
                points+=point_gain[STATS[5]]

            if race_button.draw(screen):
                race_select = True
                stat_select = False
                STATS_INIT = STATS[:]
                orc_selected = False
                elf_selected = False
                human_selected = False
                

        #Pause Menu
        if game_paused:
            functions.draw_text("Game is paused. Press ESC to unpause.", font, text_col, 100, 30, screen)
            if resume_button.draw(screen):
                game_paused = False
            if quit_button.draw(screen):
                run = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_paused = False
                if event.type == pygame.QUIT:
                    run = False
        
        for event in pygame.event.get():

            #Pause check
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = True
            #Quit check
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(60)


#RACE SELECT --------------------------------------------------------------------------------------------------------------


    while race_select and run:

        screen.fill((229,203,186))

        if not game_paused:

            disable_click = False

            #Pause button
            if pause_button.draw(screen):
                game_paused = True

            functions.draw_stats(STATS, stat_modifier, stat_font, text_col, 50, 80, 20, screen)

            #Races
            if orc_selected==False and elf_selected==False and human_selected==False:
                if orc_button.draw(screen):
                    orc_selected=True
                    STATS[0]+=2
                    STATS[2]+=1

                if elf_button.draw(screen):
                    elf_selected=True
                    STATS[1]+=2
                    STATS[4]+=1
                    pygame.time.wait(100)
                if human_button.draw(screen):
                    human_selected=True
                    for i in range(len(STATS)):
                        STATS[i]+=1
                    pygame.time.wait(100)
            
            elif (orc_selected==False and elf_selected==False and human_selected==False) == False:
                if orc_selected:

                    functions.draw_text('+2 Strength', font, (0,0,0), 50, 300, screen)
                    functions.draw_text('+1 Constitution', font, (0,0,0), 50, 330, screen)
                    functions.text_wrap('You gain a +1 bonus to attack and damage rolls with melee weapons', font, (0,0,0), screen, 50, 360, 0.5*SCREEN_WIDTH)

                    if orc_button_pressed.draw(screen):
                        orc_selected = False
                        STATS = STATS_INIT[:]
                    if elf_button.draw(screen):
                        elf_selected=True
                        orc_selected = False
                        STATS=STATS_INIT[:]
                        STATS[1]+=2
                        STATS[4]+=1
                    if human_button.draw(screen):
                        orc_selected=False
                        human_selected=True
                        STATS = STATS_INIT[:]
                        for i in range(len(STATS)):
                            STATS[i]+=1

                elif elf_selected:

                    functions.draw_text('+2 Dexterity', font, (0,0,0), 50, 300, screen)
                    functions.draw_text('+1 Wisdom', font, (0,0,0), 50, 330, screen)
                    functions.text_wrap('You gain a +1 bonus to attack and damage rolls with ranged weapons', font, (0,0,0), screen, 50, 360, 0.5*SCREEN_WIDTH)

                    if orc_button.draw(screen):
                        elf_selected=False
                        orc_selected=True
                        STATS=STATS_INIT[:]
                        STATS[0]+=2
                        STATS[2]+=1
                    if elf_button_pressed.draw(screen):
                        elf_selected=False
                        STATS = STATS_INIT[:]
                    if human_button.draw(screen):
                        elf_selected=False
                        human_selected=True
                        STATS = STATS_INIT[:]
                        for i in range(len(STATS)):
                            STATS[i]+=1

                elif human_selected:

                    functions.draw_text('+1 to all stats', font, (0,0,0), 50, 330, screen)
                    functions.text_wrap('You gain 10% more experience', font, (0,0,0), screen, 50, 360, 0.5*SCREEN_WIDTH)

                    if orc_button.draw(screen):
                        human_selected=False
                        orc_selected=True
                        STATS=STATS_INIT[:]
                        STATS[0]+=2
                        STATS[2]+=1
                    if elf_button.draw(screen):
                        human_selected=False
                        elf_selected=True
                        STATS=STATS_INIT[:]
                        STATS[1]+=2
                        STATS[4]+=1
                    if human_button_pressed.draw(screen):
                        human_selected=False
                        STATS=STATS_INIT[:]
                    
            if back_button.draw(screen):
                race_select = False
                stat_select = True
                STATS = STATS_INIT[:]
            
            if class_button.draw(screen):
                if human_selected or elf_selected or orc_selected:
                    class_select = True
                    race_select = False
                    fighter_selected = False
                    wizard_selected = False
                    [player.str, player.dex, player.con, player.int, player.wis, player.cha] = STATS
                    player.hp = 0 + int(stat_modifier[player.con])
                else:
                    functions.draw_text('Please choose a race before proceeding', font, (0,0,0), 50, 350, screen)
                    pygame.display.update()
                    pygame.time.wait(1000)
                

        #Pause Menu
        if game_paused:
            functions.draw_text("Game is paused. Press ESC to unpause.", font, text_col, 100, 30, screen)
            if resume_button.draw(screen):
                game_paused = False
            if quit_button.draw(screen):
                run = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_paused = False
                if event.type == pygame.QUIT:
                    run = False
        
        for event in pygame.event.get():

            #Pause check
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = True
            #Quit check
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(60)


#CLASS SELECT --------------------------------------------------------------------------------------------------------------
        
    while class_select and run:

        screen.fill((229,203,186))

        if not game_paused:

            functions.draw_stats(STATS, stat_modifier, stat_font, text_col, 50, 80, 20, screen)
            functions.draw_text('Health: ' + str(player.hp), font, text_col, 50, 230, screen)

            #Pause button
            if pause_button.draw(screen):
                game_paused = True

            #Class Selection
            if fighter_selected==False and wizard_selected==False:
                if fighter_button.draw(screen):
                    fighter_selected=True
                    player.hp = 10 + int(stat_modifier[player.con])
                if wizard_button.draw(screen):
                    wizard_selected = True
                    player.hp = 6 + int(stat_modifier[player.con])
                
            if fighter_selected or wizard_selected:

                if fighter_selected:
                    functions.draw_text('HP: 10 + CON base, 6 + CON per level', font, text_col, 50, 300, screen)
                    functions.draw_text('MP: 2 + WIS base, 2 + WIS per level', font, text_col, 50, 330, screen)
                    functions.text_wrap('After each combat encounter, regain 1+CON(if positive) health', font, text_col, screen, 50, 360, 600)
                    if fighter_selected_button.draw(screen):
                        fighter_selected = False
                        player.hp = 0 + int(stat_modifier[player.con])
                    if wizard_button.draw(screen):
                        fighter_selected = False
                        wizard_selected = True
                        player.hp = 6 + int(stat_modifier[player.con])

                if wizard_selected:
                    functions.draw_text('HP: 6 + CON base, 4 + CON per level', font, text_col, 50, 300, screen)
                    functions.draw_text('MP: 10 + WIS base, 10 + WIS per level', font, text_col, 50, 330, screen)
                    functions.text_wrap('After each combat encounter, regain 5+WIS(if positive) mana', font, text_col, screen, 50, 360, 600)
                    if fighter_button.draw(screen):
                        wizard_selected = False
                        fighter_selected = True
                        player.hp = 10 + int(stat_modifier[player.con])
                    if wizard_selected_button.draw(screen):
                        wizard_selected = False
                        player.hp = 0 + int(stat_modifier[player.con])

            if back_button.draw(screen):
                class_select = False
                race_select = True
                [player.str, player.dex, player.con, player.int, player.wis, player.cha] = [8,8,8,8,8,8]
                player.hp = 0
            if equipment_button.draw(screen):
                if fighter_selected or wizard_selected:
                    class_select = False
                    equipment_select = True
                    fighter_longsword = False
                    fighter_longbow = False
                    wizard_firebolt = False
                else:
                    functions.draw_text('Please choose a class before proceeding', font, (0,0,0), 50, 350, screen)
                    pygame.display.update()
                    pygame.time.wait(1000)


        #Pause Menu
        if game_paused:
            functions.draw_text("Game is paused. Press ESC to unpause.", font, text_col, 100, 30, screen)
            if resume_button.draw(screen):
                game_paused = False
            if quit_button.draw(screen):
                run = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_paused = False
                if event.type == pygame.QUIT:
                    run = False
        
        for event in pygame.event.get():

            #Pause check
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = True
            #Quit check
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(60)

#EQUIPMENT SELECT --------------------------------------------------------------------------------------------------------------

    while equipment_select and run:

        screen.fill((229,203,186))

        if not game_paused:

            functions.draw_stats([player.str, player.dex, player.con, player.int, player.wis, player.cha], stat_modifier, stat_font, text_col, 50, 80, 20, screen)
            functions.draw_text('Health: ' + str(player.hp), font, text_col, 50, 230, screen)
            functions.draw_text('AC: ' + str(player.ac()), font, text_col, 50, 260, screen)
            functions.draw_text('Current equipment:', stat_font, text_col, 50, 300, screen)
            dy = 20
            j=0
            
            if player.right_hand != None:
                functions.draw_text(player.right_hand.name, stat_font, text_col, 50, 320 + j*dy, screen)
                j+=1
            
            if player.left_hand != None:
                functions.draw_text(player.left_hand.name, stat_font, text_col, 50, 320 + j*dy, screen)
                j+=1

            if player.armor != None:
                functions.draw_text(player.armor.name, stat_font, text_col, 50, 320 + j*dy, screen)

            

            #Pause button
            if pause_button.draw(screen):
                game_paused = True

            #Fighter

            if fighter_selected:
                if player.armor != equipment.breastplate:
                    player.armor = equipment.breastplate

                if not fighter_longbow and not fighter_longsword:
                    if longsword_button.draw(screen):
                        player.spells = []
                        if player.left_hand != equipment.shield:
                            player.left_hand = equipment.shield
                        if player.right_hand != equipment.longsword:
                            player.right_hand = equipment.longsword
                        fighter_longsword = True
                    if longbow_button.draw(screen):
                        player.spells = []
                        player.left_hand = None
                        player.right_hand = equipment.longbow
                        fighter_longbow = True

                if fighter_longsword:
                    if longsword_selected_button.draw(screen):
                        player.spells = []
                        player.right_hand = None
                        player.left_hand = None
                        fighter_longsword = False

                    if longbow_button.draw(screen):
                        player.spells = []
                        player.right_hand = equipment.longbow
                        player.left_hand = None
                        fighter_longsword = False
                        fighter_longbow = True

                if fighter_longbow:
                    if longsword_button.draw(screen):
                        player.right_hand = equipment.longsword
                        player.left_hand = equipment.shield
                        player.spells = []
                        fighter_longbow = False
                        fighter_longsword = True

                    if longbow_selected_button.draw(screen):
                        player.spells = []
                        player.right_hand = None
                        fighter_longbow = False

            #Wizard
            if wizard_selected:
                if player.armor != equipment.robes:
                    player.armor = equipment.robes
                if not wizard_firebolt:
                    if firebolt_button.draw(screen):
                        player.spells.append(spellbook.firebolt)
                        player.spells.append(spellbook.fire_breath)
                        player.right_hand = equipment.dagger
                        wizard_firebolt = True
                    
                if wizard_firebolt:
                    if firebolt_selected_button.draw(screen):
                        player.spells = []
                        wizard_firebolt = False
                    

            if back_button.draw(screen):
                equipment_select = False
                class_select = True
                player.armor = None
                player.left_hand  = None
                player.right_hand = None
                player.spells = []
                fighter_longbow = False
                fighter_longsword = False
                wizard_firebolt = False

            
            if not god_mode:
                if god_mode_button.draw(screen):
                    god_mode = True
                    player.hp += 100

            elif god_mode:
                if god_mode_selected_button.draw(screen):
                    god_mode = False
                    player.hp -= 100

            if adventure_button.draw(screen):
                if fighter_longbow or fighter_longsword or wizard_firebolt:
                    equipment_select = False
                    adventure1 = True
                else:
                    functions.draw_text('Please choose your equipment before proceeding', font, (0,0,0), 50, 400, screen)
                    pygame.display.update()
                    pygame.time.wait(1000)

        #Pause Menu
        if game_paused:
            functions.draw_text("Game is paused. Press ESC to unpause.", font, text_col, 100, 30, screen)
            if resume_button.draw(screen):
                game_paused = False
            if quit_button.draw(screen):
                run = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_paused = False
                if event.type == pygame.QUIT:
                    run = False
        
        for event in pygame.event.get():

            #Pause check
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = True
            #Quit check
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(60)


# -----------------------------------------------------------------------------------------------------------------------
#CHAPTER 1 --------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
        
    if adventure1:

        player.str, player.dex, player.con, player.int, player.wis, player.cha = STATS
        player.max_hp = player.hp
        
        if fighter_selected:
            player.dnd_class = 'fighter'
            player.max_mp = 2 + int(stat_modifier[player.wis])
            player.mp = 2 + int(stat_modifier[player.wis])
            player.spell_slots = 1
            player.inventory = [equipment.shortsword, equipment.full_plate]
        elif wizard_selected:
            player.dnd_class = 'wizard'
            player.max_mp = 10 + int(stat_modifier[player.wis])
            player.mp = 10 + int(stat_modifier[player.wis])
            player.spell_slots = 3

        if orc_selected:
            player.race = 'orc'
        elif elf_selected:
            player.race = 'elf'
        elif human_selected:
            player.race = 'human'
        
        pygame.mixer.music.stop()
        pygame.mixer.music.load('Sounds/adventure_bg.mp3')
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)

    while adventure1 and run:

        screen.fill((229,203,186))


        if not game_paused:
            functions.text_wrap('You wake up from a receding nightmare. Heart pounding, you jolt upwards, then relax, realizing you\'re alone. Alone... in the middle of the woods? This isn\'t right. No, not right at all. You look around for any sign of life, yet it seems that you, and your meager adventuring equipment, are all the company you have. Suddenly, you see something small and green, rustle the leaves of the nearby bushes. A goblin!',
                                stat_font, text_col, screen, 20, 20, SCREEN_WIDTH-40)
            functions.text_wrap('It didn\'t seem to have noticed you, so you take this opportunity and follow it silently through the woods. Hoping, perhaps, that wherever this devious little creature is headed is going to hold the answers that you seek. After a short while, the goblin disappears into a small cave opening. Curious, you decide to take a peek inside.',
                                stat_font, text_col, screen, 20, 140, SCREEN_WIDTH-40)

        if dungeon_button.draw(screen):
            adventure1 = False
            dungeon1 = True

        #Pause Menu
        if game_paused:
            functions.draw_text("Game is paused. Press ESC to unpause.", font, text_col, 100, 30, screen)
            if resume_button.draw(screen):
                game_paused = False
            if quit_button.draw(screen):
                run = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_paused = False
                if event.type == pygame.QUIT:
                    run = False
        
        for event in pygame.event.get():

            #Pause check
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = True
            #Quit check
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(60)
        
    
    while dungeon1 and run:

        screen.fill((229,203,186))

        if not player.alive:
            dungeon1 = False
            start_menu = True


        #Player info
        functions.health_bar(player, 20, 20, 0, (255,255,255), screen)
        functions.xp_bar(player, 20, 20, (255,255,255), screen)
        functions.mana_bar(player, 20, 70, (255,255,255), screen)
        functions.draw_text('AC: ' + str(player.ac()), font, text_col, 50, 260, screen)
        functions.draw_text('Current equipment:', stat_font, text_col, 50, 300, screen)
        functions.draw_text('Gold: ' + str(player.gold), pygame.font.SysFont(None, 30), (0,0,0), 50, 320, screen)
        dy = 20
        j=0
        if player.right_hand != None:
            functions.draw_text(player.right_hand.name, stat_font, text_col, 50, 340 + j*dy, screen)
            j+=1
            
        if player.left_hand != None:
            functions.draw_text(player.left_hand.name, stat_font, text_col, 50, 340 + j*dy, screen)
            j+=1

        if player.armor != None:
            functions.draw_text(player.armor.name, stat_font, text_col, 50, 340 + j*dy, screen)


        DUNGEONS[0].draw(screen, player, stat_font, text_col, font, clock, run)
            #pygame.time.wait(2000)
            #dungeon2 = True
            #dungeon1 = False


        #Pause Menu
        if game_paused:
            functions.draw_text("Game is paused. Press ESC to unpause.", font, text_col, 100, 30, screen)
            if resume_button.draw(screen):
                game_paused = False
            if quit_button.draw(screen):
                run = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_paused = False
                if event.type == pygame.QUIT:
                    run = False

        if player.xp >= player.xp_to_lvlup():
            if lvlup_icon_button.draw(screen):
                functions.leveling_menu(player, font, (0,0,0), screen, clock)
        
        for event in pygame.event.get():

            #Pause check
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = True
                if event.key == pygame.K_i:
                    functions.inventory_menu(player, screen, clock, SCREEN_WIDTH, SCREEN_HEIGHT)
            #Quit check
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(60)


    while dungeon2 and run:
        screen.fill((229,203,186))

        functions.draw_text('Work in progress', font, text_col, 100, 100, screen)

        for event in pygame.event.get():

            #Pause check
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = True
            #Quit check
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(60)

pygame.quit()
