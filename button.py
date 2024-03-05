import pygame

#Button Class
class Button():
    #Initialize button as a rectangle
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.smoothscale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self, surface, on=True):
        action = False
        if on:


            #Once LMB is released, it can be pressed again
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            #Is the button doing something?
            action = False

            #Find mouse position
            position = pygame.mouse.get_pos()

            #check mouseover and clicked conditions
            #TODO: add functionality to mouseover condition
            if self.rect.collidepoint(position):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    #Button's been clicked -> it's now doing something
                    #TODO: add functionality for other clicks and not just LMB
                    action = True

        #Draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        #return whether the button is doing something or not
        return action
    

class ButtonSlow():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = True

    def draw(self, surface):
        action = False
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        position = pygame.mouse.get_pos()

        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                pygame.time.wait(200)

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
    
class ButtonOnce():
    def __init__(self, x, y, image, image_selected, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.smoothscale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

        self.image_selected = pygame.transform.smoothscale(image_selected, (int(width*scale), int(height*scale)))
        self.rect_selected = self.image_selected.get_rect()
        self.rect_selected.topleft = (x,y)

    def draw(self, surface):
        action = False
        position = pygame.mouse.get_pos()

        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                pygame.time.wait(200)

        if self.clicked:
            surface.blit(self.image_selected, (self.rect_selected.x, self.rect_selected.y))
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y))

        return action