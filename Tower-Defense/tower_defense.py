import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRASS_GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
GREY = (98, 98, 98)
DRAKE_GREY = (64, 64, 64)

pygame.init()
try:
    font = pygame.font.SysFont("Microsoft YaHei", 36)
except TypeError:
    font = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((1200, 720), pygame.RESIZABLE)
pygame.display.set_caption("塔防游戏")

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    screen.fill(GRASS_GREEN)


    pygame.draw.line(screen, BROWN, (0, 100), (300, 100), 80)
    pygame.draw.line(screen, BROWN, (260, 100), (260, 500), 80)
    pygame.draw.line(screen, BROWN, (221, 500), (750, 500), 80)
    pygame.draw.line(screen, BROWN, (710, 500), (710, 200), 80)
    pygame.draw.line(screen, BROWN, (671, 200), (1200, 200), 80)
    pygame.draw.rect(screen, DRAKE_GREY, (0, 550, 1200, 170))
    pygame.draw.rect(screen, BLACK, (45, 555, 80, 80))
    pygame.draw.rect(screen, GREY, (50, 560, 70, 70))
    pygame.draw.rect(screen, BLACK, (82, 588, 55, 15))
    pygame.draw.rect(screen, (38,38,38), (85, 590, 50, 10))
    pygame.draw.circle(screen,BLACK, (85, 595), 25)
    pygame.draw.circle(screen,(38,38,38), (85, 595), 21)
    text = font.render("Basic", True, BLACK)
    text_rect = text.get_rect()
    screen.blit(text,  (140, 560))
    text = font.render("Turret", True, BLACK)
    text_rect = text.get_rect()
    screen.blit(text, (140, 590))



    pygame.display.flip()
    clock.tick(60)

pygame.quit()
