from objects import Object3D, Vertex, Face
import numpy as np


class Cube(Object3D):
    def __init__(self, pos=(100, 100, 5, 1), size=20):
        self.vertices = [
            Vertex((-1, -1, -1, 1)), #0 TOP LEFT FRONT 
            Vertex((-1,  1, -1, 1)), #1 BOT LEFT FRONT 
            Vertex(( 1,  1, -1, 1)), #2 BOT RIGHT FRONT 
            Vertex(( 1, -1, -1, 1)), #3 TOP RIGHT FRONT 
            Vertex((-1, -1,  1, 1)), #4 TOP LEFT BACK 
            Vertex((-1,  1,  1, 1)), #5 BOT LEFT BACK 
            Vertex(( 1,  1,  1, 1)), #6 BOT RIGHT BACK 
            Vertex(( 1, -1,  1, 1))  #7 TOP RIGHT BACK 
        ]

        self.faces = [
            Face((0, 0, -1, 1), (0,0,-1,0), *self.vertices[:4:]),  #0 FRONT
            Face((0, 0,  1, 1), (0,0, 1,0), *self.vertices[4::]),  #1 BACK 
            Face((0, -1, 0, 1), (0,-1,0,0), self.vertices[0], self.vertices[4], self.vertices[7], self.vertices[3]),#2 TOP 
            Face((0,  1, 0, 1), (0, 1,0,0), self.vertices[1], self.vertices[2], self.vertices[6], self.vertices[5]),#3 BOT 
            Face((-1, 0, 0, 1), (-1,0,0,0), self.vertices[0], self.vertices[1], self.vertices[5], self.vertices[4]),#4 LEFT
            Face(( 1, 0, 0, 1), ( 1,0,0,0), self.vertices[2], self.vertices[3], self.vertices[7], self.vertices[6]) #5 RIGHT 
        ]

        super().__init__(pos, (0,0,-1,0))

        self.translate(pos)
        self.scale((size, size, size, 0))
        self.setRender()

        
    # def setRender(self):
    #     super().setRender()

    def translate(self, dist=(1, 1, 1, 0)):
        for face in self.faces:
            face.translate(dist)
        for vertex in self.vertices:
            vertex.translate(dist)
        return super().translate(dist)
    def scale(self, fact=(2, 2, 2, 0)):
        for face in self.faces:
            face.scale(fact)
        for vertex in self.vertices:
            vertex.scale(fact)
        return super().scale(fact)   
    def rotate(self, angle=(0, 0, 90, 0)):
        for face in self.faces:
            face.rotate(angle)
        for vertex in self.vertices:
            vertex.rotate(angle)
        return super().rotate(angle)

