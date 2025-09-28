import os
import sys
import time
import math
import numpy
import pygame

class collider:
    
    velocity = [0,0,0]
    
    def __init__(self,pos,size):
        self.size = [float(size[0]),float(size[1]),float(size[2])] 
        self.pos = [float(pos[0]),float(pos[1]),float(pos[2])]
    
    def requestResize(self,scene,size,positionChange):
        if(size != self.size):
            previous = self.size
            self.size = size
            self.pos = numpy.add(self.pos,positionChange)
            for box in scene[1]: 
                x = abs(box.pos[0] - self.pos[0]) - (box.size[0] + self.size[0])/2
                y = abs(box.pos[1] - self.pos[1]) - (box.size[1] + self.size[1])/2
                z = abs(box.pos[2] - self.pos[2]) - (box.size[2] + self.size[2])/2
                if(x<0 and y<0 and z<0):
                    self.size = previous
                    self.pos = numpy.subtract(self.pos,positionChange)
                    return
    
    def velocityFix(self,scene):
        self.pos = numpy.add(self.pos,self.velocity)
        for box in scene[1]: 
            x = abs(box.pos[0] - self.pos[0]) - (box.size[0] + self.size[0])/2
            y = abs(box.pos[1] - self.pos[1]) - (box.size[1] + self.size[1])/2
            z = abs(box.pos[2] - self.pos[2]) - (box.size[2] + self.size[2])/2
            if(x<0 and y<0 and z<0):
                if(x >= y and x >= z):
                    self.velocity[0] = 0
                    self.pos[0] += numpy.sign(box.pos[0] - self.pos[0])*x
                elif(y >= z):
                    self.velocity[1] = 0
                    self.pos[1] += numpy.sign(box.pos[1] - self.pos[1])*y
                else:
                    self.velocity[2] = 0
                    self.pos[2] += numpy.sign(box.pos[2] - self.pos[2])*z

class player:
    velocity = [0,0,0]
    mouseOn = False
    mouseOn_prev = False
    mouseOnCurrent = False
    Speed = 1
    jumpForce = 0.7
    grounded = False
    shift = False
    
    def __init__ (self, pos, rot, clip, focal):
        self.position = pos
        self.rotation = rot
        self.nearClip = clip
        self.focalDistance = focal
        self.box = collider(self.position,[1,2,1])
    
    def main(self,deltaTime,keys,scene):
        self.mouseOn_prev = self.mouseOn
        self.mouseOn = keys[pygame.K_t]
        if(self.mouseOn == 1 and self.mouseOn_prev == 0):
            self.mouseOnCurrent = not self.mouseOnCurrent
        mx, my = pygame.mouse.get_rel()
        if(self.mouseOnCurrent):
            pygame.mouse.set_pos(x,y)
        pygame.mouse.set_visible(not self.mouseOnCurrent)

        if(self.mouseOnCurrent):    
            self.rotation[0] -= (mx)/1000
            self.rotation[1] -= (my)/1000
            if(self.rotation[1] < -1.57079633):
                self.rotation[1] = -1.57079633
            if(self.rotation[1] > 1.57079633):
                self.rotation[1] = 1.57079633
        
        if(keys[pygame.K_w] and not self.shift):
            self.velocity[0] -= math.sin(self.rotation[0])*self.Speed* deltaTime
            self.velocity[2] += math.cos(self.rotation[0])*self.Speed* deltaTime
        if(keys[pygame.K_a] and not self.shift):
            self.velocity[0] -= math.sin(self.rotation[0]+1.57079633)*self.Speed* deltaTime
            self.velocity[2] += math.cos(self.rotation[0]+1.57079633)*self.Speed* deltaTime
        if (keys[pygame.K_s] and not self.shift):
            self.velocity[0] -= math.sin(self.rotation[0]+3.14159266)*self.Speed* deltaTime
            self.velocity[2] += math.cos(self.rotation[0]+3.14159266)*self.Speed* deltaTime
        if (keys[pygame.K_d] and not self.shift):
            self.velocity[0] -= math.sin(self.rotation[0]+4.71238899)*self.Speed* deltaTime
            self.velocity[2] += math.cos(self.rotation[0]+4.71238899)*self.Speed* deltaTime
        if (keys[pygame.K_SPACE] and self.grounded  and not self.shift):
            self.velocity[1] += self.jumpForce
            self.grounded = False
        
        #gravity
        self.velocity[1] -= 1 * deltaTime
        
        #drag
        if (keys[pygame.K_LSHIFT]):
            self.velocity = numpy.multiply(self.velocity,[1,1,1])
        else:
            self.velocity = numpy.multiply(self.velocity,[0.8,1,0.8])
        
        self.box.velocity = self.velocity
        self.box.pos = self.position
        
        if (keys[pygame.K_LSHIFT]):
            self.shift = True
            self.box.requestResize(scene,[1,1,1],[0,-0.5,0])
        else:
            self.shift = False
            self.box.requestResize(scene,[1,2,1],[0,0.5,0])

        stillColliding = self.box.velocityFix(scene)
               
        if(self.position[1] == self.box.pos[1]):
            self.grounded = True
        else:
            self.grounded = False
        
        self.position = self.box.pos
        self.velocity = self.box.velocity
    
def load(fileName): #scene format [[objects [verts],[faces],[normals],[normalRef]],[colliders x y z x y z]
    colliders = []
    objects = []
    background = []
    sceneFile = open(os.path.join(sys.path[0], fileName))
    sceneLines = [i.strip() for i in sceneFile.readlines()]
    for o in sceneLines:
        o = o.split()
        if(o[0] == "-c"):
            colliders.append(collider(o[1:4],o[4:7]))
        if(o[0] == "-b"):
            background = o[1:]
        if(o[0] == "-o"):
            verts = []
            faces = []
            normals = []
            normalRefs = []
            file = open(os.path.join(sys.path[0],os.path.join("objects",o[1])))
            lines = file.readlines()    
            for i in lines:
                i = (i.replace("/", " ")).split()
                if(i[0] == "v"):
                    verts.append([float(i[1]),float(i[2]),float(i[3])])
                
                if(i[0] == "vn"):
                    normals.append([float(i[1]),float(i[2]),float(i[3])])
                    
                if(i[0] == "f"):
                    normalRefs.append([float(i[3]),float(i[6]),float(i[9])])
                    faces.append([float(i[1]),float(i[4]),float(i[7])])
            objects.append([verts,faces,normals,normalRefs,o[2:]])
    
    return [objects,colliders,background]

def triangle(pos1,pos2,pos3,c,i):
    x1 = (player.focalDistance*pos1[0])/pos1[2]
    y1 = (player.focalDistance*pos1[1])/pos1[2]
    x2 = (player.focalDistance*pos2[0])/pos2[2]
    y2 = (player.focalDistance*pos2[1])/pos2[2]
    x3 = (player.focalDistance*pos3[0])/pos3[2]
    y3 = (player.focalDistance*pos3[1])/pos3[2]
    pygame.draw.polygon(screen, [float(c[0])*i,float(c[1])*i,float(c[2])*i], [(x1 + x, -y1 + y), (x2 + x, -y2 + y), (x3 + x, -y3 + y)])
    
def render(scene):

    rotZ = numpy.array([[math.cos(player.rotation[0]),0,math.sin(player.rotation[0])],[0,1,0],[-math.sin(player.rotation[0]),0,math.cos(player.rotation[0])]])
    rotX = numpy.array([[1,0,0],[0,math.cos(player.rotation[1]),-math.sin(player.rotation[1])],[0,math.sin(player.rotation[1]),math.cos(player.rotation[1])]])
    matrix = rotX @ rotZ
    try:
        screen.fill([float(scene[2][0]) * 255, float(scene[2][1]) * 255, float(scene[2][2]) * 255])
    except:
        pass
    for o in scene[0]: #for every thing in scene
        for m in range(len(o[1])):#for faces
        
            #scene format [[objects [verts],[faces],[normals],[normalRef]]]
            pos1 = o[0][(int(o[1][m][0]) - 1)]
            pos2 = o[0][(int(o[1][m][1]) - 1)]
            pos3 = o[0][(int(o[1][m][2]) - 1)]
            
            pos1 = numpy.subtract(pos1, player.position)
            pos2 = numpy.subtract(pos2, player.position)
            pos3 = numpy.subtract(pos3, player.position)
            
            pos1 = matrix @ pos1
            pos2 = matrix @ pos2
            pos3 = matrix @ pos3

            outside = []
            inside = []
            if pos1[2] > player.nearClip:
                outside.append(pos1)
            else:
                inside.append(pos1)
            if pos2[2] > player.nearClip:
                outside.append(pos2)
            else:
                inside.append(pos2)
            if pos3[2] > player.nearClip:
                outside.append(pos3)
            else:
                inside.append(pos3)
                            
            if (len(outside) > 0):
                #get normal vectors and transform
                normal1 = o[2][(int(o[3][m][0]) - 1)]
                normal2 = o[2][(int(o[3][m][1]) - 1)]
                normal3 = o[2][(int(o[3][m][2]) - 1)]
                faceNormal = numpy.add(normal1,normal2)
                faceNormal = numpy.add(faceNormal, normal3)
                faceNormal = numpy.divide(faceNormal,3)
                faceNormal = rotZ @ faceNormal
                faceNormal = rotX @ faceNormal
                faceNormal = faceNormal/numpy.linalg.norm(faceNormal)           
                facePos = numpy.add(pos1,pos2)
                facePos = numpy.add(facePos,pos3)
                facePos = numpy.divide(facePos,-3)
                facePos = facePos/numpy.linalg.norm(facePos)
                dotProduct = 255 * numpy.dot(faceNormal,facePos)
            
                if dotProduct > 0:             
                    if (len(outside) == 1):
                        scaleP1 = (player.nearClip-inside[0][2])/(outside[0][2]-inside[0][2])
                        scaleP2 = (player.nearClip-inside[1][2])/(outside[0][2]-inside[1][2])

                        p1 = [((outside[0][0]-inside[0][0]) * scaleP1) + inside[0][0],((outside[0][1]-inside[0][1]) * scaleP1) + inside[0][1] ,((outside[0][2]-inside[0][2]) * scaleP1) + inside[0][2]]
                        p2 = [((outside[0][0]-inside[1][0]) * scaleP2) + inside[1][0],((outside[0][1]-inside[1][1]) * scaleP2) + inside[1][1] ,((outside[0][2]-inside[1][2]) * scaleP2) + inside[1][2]]
                        
                        triangle(outside[0],p1,p2,o[4],dotProduct)
                    if (len(outside) == 2):
                        scaleP1 = (player.nearClip-inside[0][2])/(outside[0][2]-inside[0][2])
                        scaleP2 = (player.nearClip-inside[0][2])/(outside[1][2]-inside[0][2])

                        p1 = [((outside[0][0]-inside[0][0]) * scaleP1) + inside[0][0],((outside[0][1]-inside[0][1]) * scaleP1) + inside[0][1] ,((outside[0][2]-inside[0][2]) * scaleP1) + inside[0][2]]
                        p2 = [((outside[1][0]-inside[0][0]) * scaleP2) + inside[0][0],((outside[1][1]-inside[0][1]) * scaleP2) + inside[0][1] ,((outside[1][2]-inside[0][2]) * scaleP2) + inside[0][2]]
                        
                        triangle(outside[0],p1,p2,o[4],dotProduct)
                        triangle(outside[0],outside[1],p2,o[4],dotProduct)
                    if (len(outside) == 3):
                        triangle(pos1,pos2,pos3,o[4],dotProduct)

#setup
pygame.init()
screen = pygame.display.set_mode((0,0),pygame.NOFRAME)
screen.fill((0,0,0))

font = pygame.font.Font(None, 18)
text = font.render("Loading", True, (255, 255, 255))
screen.blit(text, (0, 0))
pygame.display.flip()

#game
scene1 = load("scene1")

player = player([0,0,-5],[0,0],0.1,500)
previous = 0

while 1:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if(keys[pygame.K_ESCAPE]):
        pygame.quit()
        sys.exit()
    
    x = screen.get_width()/2
    y = screen.get_height()/2  
    
    #delta time
    current = time.time()
    deltaTime = current-previous
    previous = current
    if(deltaTime>1):
        deltaTime = 0
    #Game
    player.main(deltaTime,keys,scene1)
    
    #render loop
    render(scene1)
    try:
        text = font.render("POSITION: " + (str(player.position) + "  FPS: " + str(1/deltaTime)), True, (255, 255, 255))
        screen.blit(text, (0, 0))
    except:
        pass

    pygame.display.flip() 