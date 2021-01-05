"""
high level support for doing this and that.
"""
import math
import pygame
import pygame.key

# Dynamic general game object class
from pygame.constants import *


def main():
    pygame.init()
    pygame.display.set_caption("minimal program")
    screen = pygame.display.set_mode((800, 600))

    running = True
    while running:
        screen.fill((255, 255, 255))
        pygame.draw.lines(screen, (0, 0, 0), True,[pygame.math.Vector2(20,50), pygame.math.Vector2(50,20)])
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

def toRad(angle):
    return angle*(math.pi/180)

class gameObject(object):
    def __init__(self, pos, verts, direction):
        self.pos = pos # two index array [x,y]
                           # array of points with arbitrary length,
        self.verts = verts # first and last vert will be connected
        self.rotation = 0  # Rotation represented in degrees (used for rendering)


class AsteroidsGame(object):
    def __init__(self):
        self.score = 0
        self.gameOver = False
        self.player = Player()
        self.asteroids = []
    def step(self):
        for asteroid in self.asteroids:
            if(asteroid.step):
                self.asteroids.remove(self.asteroids.index(asteroid))
        if(self.player.step() == "gameOver"):
            return "gameOver"

class Player(gameObject):
    def __init__(self):
        self.pos = [0, 0]
        self.velocity = [0, 0]
    def step(self):
        if pygame.key.get_focused():
            if pygame.key.get_pressed()[K_UP]:

            if pygame.key.get_pressed()[K_RIGHT]:

            if pygame.key.get_pressed()[K_LEFT]:

            if pygame.key.get_pressed()[K_SPACE]:


class Asteroid(gameObject):
    def __init__(self):
        self.pos = [0, 0]
        self.velocity = [0, 0]
        self.verts = self.genVerts

    def genVerts(self, vertCount):
        verts = []
        for i in range(vertCount):
            verts.append([math.cos(360/vertCount*i), math.sin(360/vertCount*i)])
        return verts


if __name__ == "__main__":
    main()
