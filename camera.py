import numpy as np
from objects import Object3D, Face
import pygame

class Camera3D(Object3D):
    def __init__(self, pos=(0, 0, 0, 1), dir=(0, 0, 1, 0), viwePort=(15, 10), fov=(60,60), zNear=1, zFar=500):
        self.viwePort = viwePort
        self.fov = fov
        self.zNear = zNear
        self.zFar = zFar

        self.projectionTransform = None
        self.transformHist = []

        super().__init__(pos, dir)

    def translate(self, dist=(1, 1, 1, 0)):
        self.transformHist.append((
            'translate', dist
        ))
        return super().translate(dist)
    def scale(self, fact=(2, 2, 2, 0)):
        self.transformHist.append((
            'scale', fact
        ))
        return super().scale(fact)
    def rotate(self, angle=(0, 0, 90, 0)):
        self.transformHist.append((
            'rotate', angle
        ))
        return super().rotate(angle)

    def inverseTransform(self):
        obj = Object3D(tuple(self.pos), tuple(self.dir))

        for t in self.transformHist[::-1]:
            if t[0] == 'translate':
                obj.translate(tuple(np.array(t[1]) * -1))
            if t[0] == 'scale':
                par = np.array(t[1], dtype=float)
                obj.scale(tuple(np.divide(par/par, par, out=np.zeros_like(par), where=par!=0)))
            if t[0] == 'rotate':
                obj.rotate(tuple(np.array(t[1]) * -1))
        return obj.transform

    def __OrthographicProjectionSpace(self):
        orthographicTransform = np.matrix([
            [1/self.viwePort[0], 0, 0, 0],
            [0, 1/self.viwePort[1], 0, 0],
            [0, 0, -(2/(self.zFar-self.zNear)), 0],
            [0, 0, -(self.zFar+self.zNear/(self.zFar-self.zNear)), 1]
        ])
        return orthographicTransform
    def __PerspectiveProjectionSpace(self):
        perspectiveTransform = np.matrix([
            [np.arctan(self.fov[0]/2), 0, 0, 0],
            [0, np.arctan(self.fov[1]), 0, 0],
            [0, 0, -(self.zFar+self.zNear/(self.zFar-self.zNear)), -1],
            [0, 0, -(2*(self.zFar+self.zNear)/(self.zFar-self.zNear)), 0]
        ])
        return perspectiveTransform
    
    def render(self, screen, style='Orthographic'):

        if style.title() == 'Orthographic':
            self.projectionTransform = self.__OrthographicProjectionSpace()
        if style.title() == 'Perspective':
            self.projectionTransform = self.__PerspectiveProjectionSpace()

        for obj in Object3D.instances:
            c = 0
            for face in obj.faces:
                if face.get_dir()[2] < 0:
                    vertices = [vertex.getProjectionSpacePosition(self).getA1() for vertex in face.vertices]
                    points = [(round(v[0]), round(v[1])) for v in vertices]
                    sorted_points = sorted(points, key = lambda x: (x[0], x[1]))
                    orderes_points = (*sorted_points[:2], *sorted_points[:1:-1]) 
                    
                    pygame.draw.polygon(screen, (0,0,0), orderes_points, 2)
                    pygame.display.flip()  
                c = c+1
        return 1
        