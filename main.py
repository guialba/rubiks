from cube import Ribiks
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))
done = False


cube = Ribiks()

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                # cube.rotate((0, 0, 15))
                cube.rotate((-15, 0, 0))
                print('Up')

            if pressed[pygame.K_DOWN]:
                cube.rotate((15, 0, 0))
                print('Down')

            if pressed[pygame.K_RIGHT]:
                cube.rotate((0, 15, 0))
                print('Right')

            if pressed[pygame.K_LEFT]:
                cube.rotate((0, -15, 0))
                print('Left')
            

            if pressed[pygame.K_p]:
                cube.rotate((0, 0, 0)) 
                print('P - TESTE')

            if pressed[pygame.K_t]:
                cube.rotateFace(45)
                print('top')
            if pressed[pygame.K_b]:
                cube.rotateFace(45, 1)
                print('bot')
            if pressed[pygame.K_n]:
                cube.rotateFace(45, 2)
                print('north')
            if pressed[pygame.K_s]:
                cube.rotateFace(45, 3)
                print('south')
            if pressed[pygame.K_w]:
                cube.rotateFace(45, 4)
                print('west')
            if pressed[pygame.K_e]:
                cube.rotateFace(45, 5)
                print('esat')

    screen.fill((255, 255, 255))

    for face in cube.render():
        pygame.draw.polygon(screen, (0,0,0,0), face['pos'], 3)
        pygame.draw.polygon(screen, face['color'], face['pos'])
        # pygame.draw.line(screen, *face['normal'], 1)
    
    pygame.display.flip()  


        
        # screen.fill((255, 255, 255))

     