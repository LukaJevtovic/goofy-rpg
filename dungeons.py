import pygame
import functions
import encounters
import numpy as np


class Dungeon():
    def __init__(self, image, x, y, scale, EVENT_POS):
        self.EVENTS = []
        self.completeness = []
        DIFFICULTIES = []

        num_encounters = len(EVENT_POS)

        #Chooses a random encounter from available ones to be the mandatory combat encounter
        mandatory_combat_index = np.random.randint(0, num_encounters-1)
        mandatory_encounter_index = mandatory_combat_index
        
        #Keeps generating a random encounter until it generates a different value than the previous one (should never do more than 2-3 iterations)
        #Then assigns the mandatory wild encounter to the given value
        while mandatory_encounter_index == mandatory_combat_index:
            mandatory_encounter_index = np.random.randint(0, num_encounters-1)

        #encounter generator
        i=0
        while i<num_encounters-1:

            #adds one combat and one wild encounter, regardless of procedural generation
            if i == mandatory_combat_index:
                DIFFICULTIES.append(1)
            elif i == mandatory_encounter_index:
                DIFFICULTIES.append(0)

            #otherwise generates a random encounter from one of the 4 difficulties (0 being a wild encounter)
            #currently 20% for a wild encounter, 40% for an easy combat encounter, 25% for a moderate combat encounter, and 15% for a hard combat encounter
            #TODO: create different distributions based on dungeon difficulty level
            else:
                chance = np.random.randint(1,101)
                if chance<=20:
                    DIFFICULTIES.append(0)
                elif 20<chance<=60:
                    DIFFICULTIES.append(1)
                elif 60<chance<=85:
                    DIFFICULTIES.append(2)
                elif 85<chance<=100:
                    DIFFICULTIES.append(3)
            
            i+=1

        #Add a mandatory boss encounter at the end of the dungeon
        DIFFICULTIES.append(4)

        i = 0
        while i < len(EVENT_POS):
            self.completeness.append(False)

            if (DIFFICULTIES[i] == 1) or (DIFFICULTIES[i] == 2) or (DIFFICULTIES[i] == 3):
                self.EVENTS.append(encounters.combat_regular(DIFFICULTIES[i], 0.11, x + scale*EVENT_POS[i][0], y + scale*EVENT_POS[i][1]))
            elif DIFFICULTIES[i] == 4:
                self.EVENTS.append(encounters.combat_boss(0.11, x + scale*EVENT_POS[i][0], y + scale*EVENT_POS[i][1]))
            elif DIFFICULTIES[i] == 0:
                self.EVENTS.append(encounters.event_regular(0.11, x + scale*EVENT_POS[i][0], y + scale*EVENT_POS[i][1]))
            else:
                print('Neki kurac se sjebo u Dungeon while petlji')

            i+=1
        

        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self, screen, player, stat_font, text_col, font, clock, run):
        
        screen.blit(self.image, (self.rect.x, self.rect.y))

        i = 0
        while i < len(self.EVENTS):

            if self.EVENTS[i].draw(screen):
                self.EVENTS[i].begin(player, screen, stat_font, text_col, font, clock, run)
                self.completeness[i] = True
            
            i+=1

        if all(self.completeness):
            return True
        else:
            return False
                

EVENT_POS = [
            [[1612, 1615], [1609, 706], [703, 427]]
            ]


#DUNGEON_POSITIONS = [
#                    [[1, 605+120, 500], [4, 375+120, 230], [0, 600+120, 270]]
#                    ]





        
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

