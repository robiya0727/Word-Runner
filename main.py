import pygame
from sys import exit

pygame.init() #start the module
screen = pygame.display.set_mode((800, 400)) #create a screen object
pygame.display.set_caption("Word Runner") #creates title
clock = pygame.time.Clock() #creates timing.
start_font = pygame.font.Font(None, 50)
background = pygame.image.load("assets/background.png").convert()


#Game loop
while True:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background, (0, 0))

    pygame.display.update()
    clock.tick(60)