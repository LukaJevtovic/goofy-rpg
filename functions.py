import pygame

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