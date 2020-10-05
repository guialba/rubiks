import weakref
import numpy as np

class Object3D():
    instances = []

    def __init__(self, pos=(0, 0, 0, 1), dir=(0, 0, 1, 0)):
        # self.__class__.instances.append(weakref.proxy(self))
        # self.__class__.instances.append(self)
        self.type = self.__class__

        self.pos = np.array(pos)
        self.dir = np.array(dir)
        self.transform = np.matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        self.rotation = self.transform
        self.translation = self.transform
        self.size = self.transform

        self.translate(pos)
    
    def setRender(self):
        self.__class__.instances.append(self)

    def translate(self, dist=(1, 1, 1, 0)):
        self.translation = self.translation * np.matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [dist[0], dist[1], dist[2], 1]
        ])
        return self.__apply_transformation()

    def scale(self, fact=(2, 2, 2, 0)):
        self.size = self.size * np.matrix([
            [fact[0], 0, 0, 0],
            [0, fact[1], 0, 0],
            [0, 0, fact[2], 0],
            [0, 0, 0, 1]
        ])

        return self.__apply_transformation()
    
    def rotate(self, angle=(0, 0, 90, 0)):
        self.rotation = self.rotation * (self.__rotateX(angle[0]) * self.__rotateY(angle[1]) * self.__rotateZ(angle[2]))
        return self.__apply_transformation()

    def __rotateX(self, angle):
        angle = angle * np.pi/180 # degree to randian 
        transform = np.matrix([
            [1, 0, 0, 0],
            [0, np.cos(angle), np.sin(angle), 0],
            [0, -np.sin(angle), np.cos(angle), 0],
            [0, 0, 0, 1]
        ])

        return transform
    def __rotateY(self, angle):
        angle = angle * np.pi/180 # degree to randian 
        transform = np.matrix([
            [np.cos(angle), 0, -np.sin(angle), 0],
            [0, 1, 0, 0],
            [np.sin(angle), 0, np.cos(angle), 0],
            [0, 0, 0, 1]
        ])

        return transform   
    def __rotateZ(self, angle):
        angle = angle * np.pi/180 # degree to randian 
        transform = np.matrix([
            [np.cos(angle), np.sin(angle), 0, 0],
            [-np.sin(angle), np.cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        return transform   

    def __apply_transformation(self):
        self.transform = self.size * self.rotation * self.translation
        return self.transform

    def get_pos(self):
        return self.__getWorldSpacePosition().getA1() 
    def get_dir(self):
        return self.__getWorldSpaceDirection().getA1() 

    def __getWorldSpacePosition(self):
        return self.pos * self.transform
    def __getWorldSpaceDirection(self):
        return self.dir * self.transform

    def __getViewSpacePosition(self, camera):
        return self.__getWorldSpacePosition() * camera.inverseTransform()
    def __getViewSpaceDirection(self, camera):
        return self.__getWorldSpaceDirection() * camera.inverseTransform()

    def getProjectionSpacePosition(self, camera):
        return self.__getViewSpacePosition(camera) * camera.projectionTransform
    def getPojectionSpaceDirection(self, camera):
        return self.__getViewSpaceDirection(camera) * camera.projectionTransform

class Vertex(Object3D):
    def __init__(self, pos=(0, 0, 0, 1)):
        super().__init__(pos)

class Face(Object3D):
    def __init__(self, pos=(0, 0, 0, 1), normal=(0,0,1,0), *vertices):
        self.vertices = vertices
        super().__init__(pos, normal)

        