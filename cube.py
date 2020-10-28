import numpy as np

class Cube:
    def __init__(self, scale=1):
        self.size = scale
        self.transform = np.identity(4)
        self.origin=(0,0,0,1)
        self.vertices = np.matrix([
            [0, 0, 0, 1], #0 TOP LEFT FRONT 
            [0, scale, 0, 1], #1 BOT LEFT FRONT 
            [scale, scale, 0, 1], #2 BOT RIGHT FRONT 
            [scale, 0, 0, 1], #3 TOP RIGHT FRONT 
            [0, 0, scale, 1], #4 TOP LEFT BACK 
            [0, scale, scale, 1], #5 BOT LEFT BACK 
            [scale, scale, scale, 1], #6 BOT RIGHT BACK 
            [scale, 0, scale, 1]  #7 TOP RIGHT BACK 
        ])
        self.faces = [
            [0,1,2,3], #0 FRONT
            [7,6,5,4], #1 BACK
            [4,0,3,7], #2 TOP 
            [1,5,6,2], #3 BOT 
            [4,5,1,0], #4 LEFT
            [3,2,6,7]  #5 RIGHT 
        ]
    def moveOrigin(self, dist):
        translation = np.matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [dist[0], dist[1], dist[2], 1]
        ])
        self.origin = np.array(self.origin) * translation
        self.origin = list(self.origin.getA1())

    def setOrigin(self, new):
        ori = [*new, 1] if len(new) == 3 else new
        self.origin = ori

    
    def move(self, dist):
        translation = np.matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [dist[0], dist[1], dist[2], 1]
        ])
        self.transform = self.transform * self.moveToOrigin() * translation * self.moveToOrigin(True)
        self.moveOrigin(dist)
        return translation

    def rotate(self, angle):
        # angle = angle * np.pi/180 # degree to randian 
        radian = (
            angle[0] * np.pi/180,
            angle[1] * np.pi/180,
            angle[2] * np.pi/180
        )
        
        rotation =  np.matrix([
                [1, 0, 0, 0],
                [0, np.cos(radian[0]), np.sin(radian[0]), 0],
                [0, -np.sin(radian[0]), np.cos(radian[0]), 0],
                [0, 0, 0, 1]
            ]) * np.matrix([
                [np.cos(radian[1]), 0, -np.sin(radian[1]), 0],
                [0, 1, 0, 0],
                [np.sin(radian[1]), 0, np.cos(radian[1]), 0],
                [0, 0, 0, 1]
            ]) * np.matrix([
                [np.cos(radian[2]), np.sin(radian[2]), 0, 0],
                [-np.sin(radian[2]), np.cos(radian[2]), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])

        self.transform = self.transform * self.moveToOrigin() * rotation * self.moveToOrigin(True)
        return rotation
 
    def scale(self, fact):
        size = np.matrix([
            [fact[0], 0, 0, 0],
            [0, fact[1], 0, 0],
            [0, 0, fact[2], 0],
            [0, 0, 0, 1]
        ])
        self.transform = self.transform * self.moveToOrigin() * size * self.moveToOrigin(True)
        return size
 
    def applyTransformation(self, transform):
        self.transform = self.transform * self.moveToOrigin() * transform * self.moveToOrigin(True)
 
    def moveToOrigin(self, ida=False):
        translation = np.matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [self.origin[0] * (1 if ida else -1), self.origin[1] * (1 if ida else -1), self.origin[2] * (1 if ida else -1), 1]
        ])
        return translation

    def getFaceCenter(self, face):
        p1 = self.applyTransform()[face[0]].getA1()
        p2 = self.applyTransform()[face[1]].getA1()
        p3 = self.applyTransform()[face[2]].getA1()
        p4 = self.applyTransform()[face[3]].getA1()

        f = np.matrix([p1,p2,p3,p4])
        
        return np.mean(f, axis=1)

    def getFaceNormal(self, face):
        p1 = self.applyTransform()[face[0]].getA1()
        p2 = self.applyTransform()[face[1]].getA1()
        p3 = self.applyTransform()[face[2]].getA1()

        l1 = np.array(p2[:3]) - np.array(p1[:3])
        l2 = np.array(p3[:3]) - np.array(p1[:3])
        normal = np.cross(l1, l2)
        l = np.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
        
        return normal/l if l>0 else normal

    def getNormals(self):
        return [self.getFaceNormal(face) for face in self.faces]

    def applyTransform(self):
        return self.vertices * self.transform 
    
    def render(self):
        nearPlane = 1
        farPlane = 1000
        fieldOfViewAngle = 90
        aspectRation = 600/800
        fieldOfView = np.arctan(np.radians(fieldOfViewAngle))
        zDiff = farPlane - nearPlane
        
        projectionMatrix = np.matrix([
            [aspectRation * fieldOfView, 0, 0, 0],
            [0, fieldOfView, 0, 0],
            [0, 0, farPlane / zDiff, 1],
            [0, 0, (farPlane * nearPlane * -1) / zDiff, 0]
        ])

        trandformed = self.applyTransform()
        trandformed += np.array([0,0,1,0])

        projected = trandformed * projectionMatrix

        projectedVertices = [
            (
                ((v[0] if v[3] == 0 else v[0]/v[3]) + 1) * 200,
                ((v[1] if v[3] == 0 else v[1]/v[3]) + 1) * 200
            )
            for v in projected.getA()
        ]
        return [
            {
                "face": face,
                # "normal": ( self.getFaceCenter(face), self.getFaceCenter(face) * self.getFaceNormal(face) ),
                "pointsInWorld": [trandformed[f].getA1() for f in face],
                "color": (0,0,0,0),
                "pos": (
                    projectedVertices[face[0]], 
                    projectedVertices[face[1]],
                    projectedVertices[face[2]],
                    projectedVertices[face[3]]
                )
            }
            for face in self.faces if np.dot(self.getFaceNormal(face), np.array(trandformed[face[0]].getA1()[:3]) - np.array([0,0,0]))<0
        ]

class Cubie(Cube):
    def __init__(self):
        super().__init__()
        self.mark = False

    def setMark(self, mark):
        self.mark = mark

    def setId(self, id):
        self.id = id

    
    def getFaceColor(self, face):
        colors = [
            (200,220,0,255), #yellow
            (255,255,255,255), #white
            (30,30,255,255), #blue
            (0,150,50,255), #green
            (200,0,0,255), #red
            (250,100,0,255), #orange
            (0,0,0,0) #black
        ]

        face_id = [i for i, f in enumerate(self.faces) if f == face][0] if not self.mark else -1
        return colors[face_id]
    
    def render(self):
        faces = super().render()
        for face in faces:
            face['color'] = self.getFaceColor(face['face'])
        return faces


class Ribiks:
    def __init__(self):
        self.cubies = [Cubie() for i in range(27)]
        self.originOffset = 1.5
        self.origin = (self.originOffset, self.originOffset, 5+self.originOffset)
        self.transform = np.identity(4)
        
        self.faces = [
            (0, -1, 0), #top
            (0, 1, 0), #bot
            (0, 0, -1), #north
            (0, 0, 1), #south
            (-1, 0, 0), #west
            (1, 0, 0)  #east
        ]

        i = 0
        for l in range(3):
            for c in range(3):
                for p in range(3):
                    self.cubies[i].setId((l-1, c-1, p-1))
                    self.cubies[i].move((l, c, 5+p))
                    i += 1
        for c in self.cubies:
            c.setOrigin(self.origin)

        # self.cubies[0].setMark(True)

        
    
    def move(self, dist):
        for c in self.cubies:
            transform = c.move(dist)
        # self.transform = self.transform * transform
    def scale(self, fact):
        for c in self.cubies:
            transform = c.scale(fact)
        # self.transform = self.transform * transform
    def rotate(self, angle):
        for c in self.cubies:
            transform = c.rotate(angle)
        self.transform = self.transform * transform
    def moveToOrigin(self, ida=False):
        translation = np.matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [self.origin[0] * (1 if ida else -1), self.origin[1] * (1 if ida else -1), self.origin[2] * (1 if ida else -1), 1]
        ])
        return translation


    def rotateFace(self, angle, faceToRotate=0):
        face = self.faces[faceToRotate]

        for cubie in self.cubies:
            mask = [bool(i) for i in face]
            if np.array(cubie.id)[mask] == np.array(face)[mask]:
                
                norm = np.array([*face, 1])
                vw = (norm * np.matrix(self.transform)).getA1()
                radian = angle * np.pi/180

                rodrigues = np.matrix([
                    [
                        np.cos(radian) + np.power(vw[0],2)*(1-np.cos(radian)), 
                        vw[2]*np.sin(radian) + vw[0]*vw[1]*(1-np.cos(radian)),
                        -vw[1]*np.sin(radian) + vw[0]*vw[2]*(1-np.cos(radian)),
                        0
                    ],
                    [
                        vw[0]*vw[1]*(1-np.cos(radian)) - vw[2]*np.sin(radian),
                        np.cos(radian) + np.power(vw[1],2)*(1-np.cos(radian)), 
                        vw[0]*np.sin(radian) + vw[1]*vw[2]*(1-np.cos(radian)),
                        0
                    ],
                    [
                        vw[1]*np.sin(radian) + vw[0]*vw[2]*(1-np.cos(radian)),
                        -vw[0]*np.sin(radian) + vw[1]*vw[2]*(1-np.cos(radian)),
                        np.cos(radian) + np.power(vw[2],2)*(1-np.cos(radian)), 
                        0
                    ],
                    [0,0,0,1]
                    
                ])
                
                cubie.applyTransformation(rodrigues)
               

                c = Cube()
                rotation = c.rotate(np.array(face)*angle)
                newId = np.array([*cubie.id, 1]) * rotation
                cubie.setId(tuple(np.around(newId).getA1()[:-1]))




    def render(self):
        faces = []
        for c in self.cubies:
            for face in c.render():
                face['midZ'] = sum(point[2] for point in face['pointsInWorld'])/4
                faces.append(face)

        orderedFaces = sorted(faces, key = lambda obj: obj['midZ'])
        return orderedFaces[::-1]