from cube import Cube
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))
done = False


cube = Cube()

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()

            val = 1

            if pressed[pygame.K_UP]:
                # cube.rotate((0, 0, 15))
                cube.move((0, -val, 0))
                print('Up')

            if pressed[pygame.K_DOWN]:
                cube.move((0, val, 0))
                print('Down')

            if pressed[pygame.K_RIGHT]:
                cube.move((val, 0, 0))
                print('Right')

            if pressed[pygame.K_LEFT]:
                cube.move((-val, 0, 0))
                print('Left')


            if pressed[pygame.K_w]:
                cube.move((0, 0,val))
                print('w')
            if pressed[pygame.K_s]:
                cube.move((0, 0,-val))
                print('s')
            

            val = 30
            if pressed[pygame.K_i]:
                val *= -1
                print('i')

            if pressed[pygame.K_y]:
                cube.rotate((0, val, 0))
                print('y')
            if pressed[pygame.K_x]:
                cube.rotate((val, 0, 0))
                print('x')
            if pressed[pygame.K_z]:
                cube.rotate((0, 0, val))
                print('z')
            

    screen.fill((255, 255, 255))

    for face in cube.render():
        pygame.draw.polygon(screen, (0,0,0,0), face['pos'], 3)
        pygame.draw.polygon(screen, (200, 200, 0, 255), face['pos'])
        # pygame.draw.line(screen, *face['normal'], 1)
    
    pygame.display.flip()  


        
        # screen.fill((255, 255, 255))

     