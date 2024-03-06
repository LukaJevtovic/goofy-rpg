import pygame
import equipment
import creatures
import functions
import numpy as np

stat_modifier = {1:'-5', 2:'-4', 3:'-4', 4:'-3', 5:'-3', 6:'-2', 7:'-2', 8:'-1', 9:'-1', 10:'+0', 11:'+0', 12:'+1', 13:'+1', 14:'+2', 15:'+2', 16:'+3', 17:'+3', 18:'+4', 19:'+4', 20:'+5', 21:'+5', 22:'+6', 23:'+6', 24:'+7', 25:'+7'}

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

class combat_regular():
    def __init__(self, difficulty, scale, x, y):

        self.x = x
        self.y = y
        self.scale = scale
        self.difficulty = difficulty

        image_name = 'Pictures/combat' + str(difficulty) + '.png'
        image = pygame.image.load(image_name).convert_alpha()
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.clicked = False
        self.completed = False

    def draw(self, surface):


        if not self.completed:
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            position = pygame.mouse.get_pos()

            if self.rect.collidepoint(position):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    self.completed = True
                    image_name = 'Pictures/combat' + str(self.difficulty) + '_completed.png'
                    image = pygame.image.load(image_name).convert_alpha()
                    width = image.get_width()
                    height = image.get_height()
                    self.image = pygame.transform.scale(image, (int(width*self.scale), int(height*self.scale)))
                    return True
                
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def begin(self, player, screen, stat_font, text_col, font, clock, run):

        COMBAT1, irrelevant = initiate_encounter_lists()

        if self.difficulty == 1:
            if len(COMBAT1)>1:
                j = np.random.randint(0, len(COMBAT1)-1)
            else:
                j=0
            ENEMIES = COMBAT1[j]

        functions.combat(player, ENEMIES, screen, stat_font, text_col, font, clock, run)

        if player.alive:

            if player.dnd_class == 'fighter':

                if int(stat_modifier[player.con])>0:
                    con_bonus = int(stat_modifier[player.con])
                else:
                    con_bonus = 0

                if player.hp+1+con_bonus >= player.max_hp:
                    player.hp = player.max_hp
                else:
                    player.hp+=1+con_bonus

                if int(stat_modifier[player.wis])>0:
                    wis_bonus = int(stat_modifier[player.wis])
                else:
                    wis_bonus = 0
                if player.mp+1+wis_bonus>=player.max_mp:
                    player.mp = player.max_mp
                else:
                    player.mp+=1+wis_bonus


            elif player.dnd_class == 'wizard':

                if int(stat_modifier[player.wis])>0:
                    wis_bonus = int(stat_modifier[player.wis])
                else:
                    wis_bonus = 0

                if player.mp+5+wis_bonus>=player.max_mp:
                    player.mp = player.max_mp
                else:
                    player.mp+=5+wis_bonus


            functions.loot_menu(player, self.difficulty, screen, clock)



class combat_boss():
    def __init__(self, scale, x, y):

        self.x = x
        self.y = y
        self.scale = scale

        image_name = 'Pictures/combat_boss.png'
        image = pygame.image.load(image_name).convert_alpha()
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.clicked = False
        self.completed = False

    def draw(self, surface):


        if not self.completed:
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            position = pygame.mouse.get_pos()

            if self.rect.collidepoint(position):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    self.completed = True
                    image_name = 'Pictures/combat_boss_completed.png'
                    image = pygame.image.load(image_name).convert_alpha()
                    width = image.get_width()
                    height = image.get_height()
                    self.image = pygame.transform.scale(image, (int(width*self.scale), int(height*self.scale)))
                    return True


        surface.blit(self.image, (self.rect.x, self.rect.y))

    def begin(self, player, screen, stat_font, text_col, font, clock, run):
        irrelevant, COMBAT_BOSS = initiate_encounter_lists()

        if len(COMBAT_BOSS)>1:
            j = np.random.randint(0, len(COMBAT_BOSS))
        else:
            j=0

        ENEMIES = COMBAT_BOSS[j]

        functions.combat(player, ENEMIES, screen, stat_font, text_col, font, clock, run)

        if player.alive:
            if player.dnd_class == 'fighter':

                if int(stat_modifier[player.con])>0:
                    con_bonus = int(stat_modifier[player.con])
                else:
                    con_bonus = 0

                if player.hp+1+con_bonus >= player.max_hp:
                    player.hp = player.max_hp
                else:
                    player.hp+=1+con_bonus

                if int(stat_modifier[player.wis])>0:
                    wis_bonus = int(stat_modifier[player.wis])
                else:
                    wis_bonus = 0
                if player.mp+1+wis_bonus>=player.max_mp:
                    player.mp = player.max_mp
                else:
                    player.mp+=1+wis_bonus


            elif player.dnd_class == 'wizard':

                if int(stat_modifier[player.wis])>0:
                    wis_bonus = int(stat_modifier[player.wis])
                else:
                    wis_bonus = 0

                if player.mp+5+wis_bonus>=player.max_mp:
                    player.mp = player.max_mp
                else:
                    player.mp+=5+wis_bonus

            functions.loot_menu(player, 4, screen, clock)



class event_regular():
    def __init__(self, scale, x, y):

        self.x = x
        self.y = y
        self.scale = scale

        image_name = 'Pictures/event.png'
        image = pygame.image.load(image_name).convert_alpha()
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.clicked = False
        self.completed = False

    def draw(self, surface):


        if not self.completed:
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            position = pygame.mouse.get_pos()

            if self.rect.collidepoint(position):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    self.completed = True
                    image_name = 'Pictures/event_completed.png'
                    image = pygame.image.load(image_name).convert_alpha()
                    width = image.get_width()
                    height = image.get_height()
                    self.image = pygame.transform.scale(image, (int(width*self.scale), int(height*self.scale)))
                    return True


        surface.blit(self.image, (self.rect.x, self.rect.y))

    def begin(self, player, screen, stat_font, text_col, font, clock, run):
        
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

        functions.text_wrap('A wise man that hangs around in the dungeon shares his wisdoms! You gain 150xp (Work in progress)', font, text_col, screen, 100, 100, SCREEN_WIDTH-200)
        player.xp+=150
        pygame.display.update()
        pygame.time.wait(4000)


def initiate_encounter_lists():
    COMBAT1 = [[creatures.basic_enemy(*creatures.goblin_stats)]]

    COMBAT_BOSS = [[creatures.basic_enemy(*creatures.goblin_stats), creatures.basic_enemy(*creatures.goblin_stats)], [creatures.basic_enemy('Goblin brute', 100, 18, 9, 16, 8, 16, 8, 8, 8, equipment.longsword, 4)]]

    return COMBAT1, COMBAT_BOSS


#
