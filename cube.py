import pygame
import numpy as np

class Cube:
    def __init__(self, pos=(300, 300, 50), size=50):
        self.size = size
        self.pos = np.array(pos)
        self.rotation = np.array([0, 0, 0])
        
        
        self.vertices = np.matrix([
            [-1, -1, -1],   #0- top left front
            [-1, 1, -1],    #1- bot left front        
            [1, 1, -1],     #2- bot right front
            [1, -1, -1],    #3- top right front
            [1, -1, 1],     #4- top right back
            [1, 1, 1],      #5- bot right back
            [-1, 1, 1],     #6- bot left back 
            [-1, -1, 1],    #7- top left back
        ])
        self.faces = np.array([
            [0, 1, 2, 3], # front
            [7, 0, 3, 4], # top
            [4, 5, 6, 7], # back
            [1, 6, 5, 2], # bot
            [3, 2, 5, 4], # right
            [7, 6, 1, 0], # left
        ])

        self.face_colors = [
            (20,200,0), #yellow
            (0,50,255), #blue
            (0,0,0), #black
            (100,200,50), #green
            (150,230,0), #orange
            (255,20,0) #red
        ]

        #scale
        self.vertices = self.vertices * (self.size/2)
        
        ##tilt
        # self.rotate((45, 45, 0))  

    def __calculate_positions(self):  
        return (self.vertices + self.pos)

    def __orthographic_projection(self):
        scale = np.matrix([
            [1, 0, 0],
            [0, 0, 1]
        ])

        offset = np.matrix([[1, 1]]).getT()

        points = self.__calculate_positions().getT()

        view = scale * points + offset

        return view.getT().getA()
    
    
    def get_visibleFaces(self):
        mean = []
        for face in self.faces:
            points = [self.__calculate_positions()[v] for v in face]
            mean.append(np.mean(points, axis=0))
        meanZ = [list(m)[0][2] for m in mean]    
        
        # print(np.argsort(meanZ)[:-4:-1])
        return np.argsort(meanZ)[:-4]


    def rotate(self, angle=(0, 30, 0)):
        alpha = np.array(angle)[2]
        beta = np.array(angle)[1]
        gama = np.array(angle)[0]

        r = np.matrix([
            [
                round(np.cos(alpha)) * round(np.cos(beta)),
                round(np.cos(alpha)) * round(np.sin(beta)) * round(np.sin(gama)) -  round(np.sin(alpha)) * round(np.cos(gama)),
                round(np.cos(alpha)) * round(np.sin(beta)) * round(np.cos(gama)) + round(np.sin(alpha)) * round(np.sin(gama))
            ],
            [
                round(np.sin(alpha)) * round(np.cos(beta)),
                round(np.sin(alpha)) * round(np.sin(beta)) * round(np.sin(gama)) +  round(np.cos(alpha)) * round(np.cos(gama)),
                round(np.sin(alpha)) * round(np.sin(beta)) * round(np.cos(gama)) - round(np.cos(alpha)) * round(np.sin(gama))
            ],
            [
                -round(np.sin(beta)),
                round(np.cos(beta)) * round(np.sin(gama)),
                round(np.cos(beta)) * round(np.cos(gama))
            ]
        ])

        self.vertices = (r * self.vertices.getT()).getT()
    def rotateAxis(self, angle=15, axis='z'):
        
        rotation_matrix = {
            'x' : np.matrix([
                [ 1, 0, 0 ],
                [ 0, round(np.cos(angle)), -round(np.sin(angle)) ],
                [ 0, round(np.sin(angle)), round(np.cos(angle)) ]
            ]),
            'y' : np.matrix([
                [ round(np.cos(angle)), 0, round(np.sin(angle)) ],
                [ 0, 1, 0 ],
                [ -round(np.sin(angle)), 0, round(np.cos(angle)) ]
            ]),
            'z' : np.matrix([
                [ round(np.cos(angle)), -round(np.sin(angle)), 0 ],
                [ round(np.sin(angle)), round(np.cos(angle)), 0 ],
                [ 0, 0, 1 ]
            ])
        }
        self.vertices = (rotation_matrix[axis] * self.vertices.getT()).getT()




    def draw(self, screen):
        for face in self.get_visibleFaces():
            vertices = self.faces[face]
            points = [list(self.__orthographic_projection()[v]) for v in vertices]

            print(face)
            #print(vertices)
            #print(self.__orthographic_projection())
            # t = np.array([self.pos[0], self.pos[1]])
            # print(np.array(points)/self.size/2 - t)
            pygame.draw.polygon(screen, self.face_colors[face], points)





