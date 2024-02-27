import pygame
import equipment
import creatures
import functions
import numpy as np

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

    def begin(self, player, screen, stat_font, text_col, font, clock):
        if self.difficulty == 1:
            if len(COMBAT1)>1:
                j = np.random.randint(0, len(COMBAT1)-1)
            else:
                j=0
            ENEMIES = COMBAT1[j]

        functions.combat(player, ENEMIES, screen, stat_font, text_col, font, clock)



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

    def begin(self, player, screen, stat_font, text_col, font, clock):

        if len(COMBAT_BOSS)>1:
            j = np.random.randint(0, len(COMBAT_BOSS)-1)
        else:
            j=0

            ENEMIES = COMBAT_BOSS[j]

        functions.combat(player, ENEMIES, screen, stat_font, text_col, font, clock)



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

    def begin(self, player, screen, stat_font, text_col, font, clock):
        
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

        functions.draw_text('You find a lost pouch of gold! (Work in progress)', font, text_col, 100, 100, screen)
        player.equipment.append(equipment.gold_pouch)
        pygame.display.update()
        pygame.time.wait(4000)


COMBAT1 = [[creatures.basic_enemy(*creatures.goblin_stats)]]

COMBAT_BOSS = [[creatures.basic_enemy(*creatures.goblin_stats), creatures.basic_enemy(*creatures.goblin_stats), creatures.basic_enemy(*creatures.goblin_stats)]]

