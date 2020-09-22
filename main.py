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
        
        if event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                c.rotateAxis(15, 'y')
            if pressed[pygame.K_DOWN]:
                c.rotateAxis(15, 'z')
            if pressed[pygame.K_RIGHT]:
                c.rotateAxis(15, 'x')
            if pressed[pygame.K_LEFT]:
                print('None')

        screen.fill((255, 255, 255))
        c.draw(screen)

    pygame.display.flip()   