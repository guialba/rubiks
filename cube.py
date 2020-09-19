import pygame
import numpy as np

class Cube:
    def __init__(self, pos=(300, 300, 50), size=10):
        self.size = size
        self.pos = np.array(pos)
        self.vertices = np.matrix([
            [-1, -1, -1],   #0- top left front
            [-1, 1, -1],    #1- bot left front        
            [1, 1, -1],     #2- bot right front
            [1, -1, -1],     #3- top right front
            [-1, -1, 1],    #4- top left back
            [-1, 1, 1],     #5- bot left back 
            [1, 1, 1],      #6- bot right back
            [1, -1, 1]      #7- top right back
        ])
        self.faces = np.array([
            [0, 1, 2, 3], # front
            [0, 3, 4, 7], # top
            [4, 5, 6, 7], # back
            [1, 2, 5, 6], # bot
            [2, 3, 6, 7], # right
            [0, 1, 4, 5], # left
        ])

        self.face_colors = [
            (20,200,0),
            (0,50,255),
            (0,0,0),
            (50,255,50),
            (150,230,0),
            (255,20,0)
        ]

    def __calculate_positions(self):  
        return self.vertices * (self.size/2) + self.pos

    def __orthographic_projection(self):
        scale = np.matrix([
            [1, 0],
            [0, 1],
            [0, 0]
        ]).getT()

        offset = np.matrix([[1, 1]]).getT()

        points = self.__calculate_positions().getT()

        view = scale  * points + offset

        return view.getT().getA()
    
    
    def get_visibleFaces(self):
        return (0, 1, 2)

    def draw(self, screen):
        for face in self.get_visibleFaces():
            vertices = self.faces[face]
            points = [self.__orthographic_projection()[v] for v in vertices]

            print(vertices)
            print(self.__orthographic_projection())
            print(points)
            pygame.draw.polygon(screen, self.face_colors[face], points)





