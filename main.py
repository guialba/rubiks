import pygame

from cube import Cube

pygame.init()

screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))
done = False

c = Cube()
c.draw(screen)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    

    pygame.display.flip()   