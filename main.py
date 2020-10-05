from cube import Cube
from camera import Camera3D
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))
done = False

camera = Camera3D()
cube = Cube()

camera.render(screen, 'Perspective')
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                print('Up')
                cube.rotate((0,30,0,0))

            if pressed[pygame.K_DOWN]:
                print('Down')
                cube.rotate((0,0,30,0))

            if pressed[pygame.K_RIGHT]:
                print('Right')
                cube.rotate((30,0,0,0))

            if pressed[pygame.K_LEFT]:
                print('Left')
                cube.rotate((0,0,0,0))

            screen.fill((255, 255, 255))
            camera.render(screen, 'Perspective')

        
        # screen.fill((255, 255, 255))

     