import pygame
import functions
import encounters
import numpy as np


class Dungeon():
    def __init__(self, image, x, y, scale, EVENTS):
        self.EVENTS = []
        self.completeness = []

        i = 0
        while i < len(EVENTS):
            self.completeness.append(False)

            if (EVENTS[i][0] == 1) or (EVENTS[i][0] == 2) or (EVENTS[i][0] == 3):
                j = np.random.randint(0, len(encounters.COMBAT1))
                self.EVENTS.append(encounters.combat_regular(EVENTS[i][0], 0.11, EVENTS[i][1], EVENTS[i][2]))
            elif EVENTS[i][0] == 4:
                self.EVENTS.append(encounters.combat_boss(0.11, EVENTS[i][1], EVENTS[i][2]))
            elif EVENTS[i][0] == 0:
                self.EVENTS.append(encounters.event_regular(0.11, EVENTS[i][1], EVENTS[i][2]))
            else:
                print('Neki kurac se sjebo u Dungeon while petlji')

            i+=1
        

        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def draw(self, screen, player, stat_font, text_col, font, clock):
        
        screen.blit(self.image, (self.rect.x, self.rect.y))

        i = 0
        while i < len(self.EVENTS):

            if self.EVENTS[i].draw(screen):
                self.EVENTS[i].begin(player, screen, stat_font, text_col, font, clock)
                self.completeness[i] = True
            
            i+=1

        if all(self.completeness):
            return True
        else:
            return False
                

DUNGEON_POSITIONS = [
                    [[1, 605+120, 500], [4, 375+120, 230], [0, 600+120, 270]]
                    ]





        
# TESTING AREA

"""
       
pygame.init()




#Screen setup
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

INTRO_POSITIONS = [[1, 605, 500], [4, 375, 230], [0, 600, 270]]

dungeon_img = pygame.image.load('Dungeons/intro_dungeon.jpg').convert_alpha()

intro_dungeon = Dungeon(dungeon_img, 500, 400, 0.25, INTRO_POSITIONS)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    intro_dungeon.draw(screen)

    pygame.display.update()


"""

