import math
import pygame
import pygame.key
import random

# Dynamic general game object class
from pygame.constants import *


class Display(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Python Asteroids")
        self.screen = pygame.display.set_mode((800, 600))

    def draw(self, game_object):
        vectors_to_draw = []
        for vert in game_object.verts:
            print(vert.x, vert.y)
            vectors_to_draw.append(pygame.Vector2(game_object.pos.x + vert.x, game_object.pos.y + vert.y))

        pygame.draw.polygon(self.screen, (255, 255, 255), vectors_to_draw)


def toRad(angle):
    return angle * (math.pi / 180)


class vector2(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

    def copy(self):
        return vector2(self.x, self.y)

    def add(self, vec2):
        self.x += vec2.x
        self.y += vec2.y

    def invert(self):
        self.x *= -1
        self.y *= -1

    def dot_product(self, vec2):
        self.x *= vec2.x
        self.y *= vec2.y

    def multiply(self, factor):
        return vector2(self.x * factor, self.y * factor)

    def rotate(self, rads):
        x = self.x * math.cos(rads) - self.y * math.sin(rads)
        y = self.x * math.sin(rads) + self.y * math.cos(rads)
        return vector2(x, y)


class gameObject(object):
    def __init__(self, pos, verts, direction):
        self.pos = pos
        self.verts = verts  # first and last vert will be connected
        self.direction = direction  # Rotation represented in degrees (used for rendering)


class AsteroidsGame(object):
    def __init__(self):
        self.score = 0
        self.gameOver = False
        self.player = Player()
        self.asteroids = []
        self.turn_speed = 5  # degrees per frame

        self.display = Display()

    def step(self):
        self.display.screen.fill((0, 0, 0))
        for asteroid in self.asteroids:
            if not asteroid.step:
                self.asteroids.remove(self.asteroids.index(asteroid))

        if self.player.step() == "gameOver":
            return "gameOver"
        self.display.draw(self.player)

        for asteroid in self.asteroids:
            self.display.draw(asteroid)


class Player(gameObject):
    def __init__(self):
        self.pos = vector2(200, 400)
        self.velocity = vector2(0, 0)
        self.direction = toRad(180+90)

        self.verts = [
            vector2(7, 0),
            vector2(-4, -4),
            vector2(0, 0),
            vector2(-4, 4),
            vector2(7, 0)
        ]


    def step(self):
        if pygame.key.get_focused():
            if pygame.key.get_pressed()[K_UP]:
                self.apply_thrust()
                pass
            if pygame.key.get_pressed()[K_RIGHT]:
                pass
            if pygame.key.get_pressed()[K_LEFT]:
                pass
            if pygame.key.get_pressed()[K_SPACE]:
                pass
        self.apply_velocity()
        self.apply_friction()

    def apply_thrust(self):
        thrust_vector = vector2(math.cos(self.direction), math.sin(self.direction))
        self.velocity.add(thrust_vector)

    def apply_friction(self):
        self.velocity.x = self.velocity.x * 0.98
        self.velocity.y = self.velocity.y * 0.98

    def turn(self, dir):  # dir from 1 to -1 for right and left
        self.rotation += dir * self.turn_speed

    def apply_velocity(self):
        self.pos.add(self.velocity.multiply(1/60))


class Asteroid(gameObject):
    def __init__(self):
        self.pos = [0, 0]
        self.velocity = [0, 0]
        self.verts = self.gen_verts(16)

    def gen_verts(self, vertCount):
        verts = []
        for i in range(vertCount):
            amplitude = random.random()
            current_rad = (2 * math.pi / vertCount * i)
            verts.append([math.cos(current_rad) * amplitude, math.sin(current_rad) * amplitude])
        return verts


def main():
    gamestate = AsteroidsGame()
    running = True
    game_over = False
    while running:
        pygame.display.update()
        gamestate.step()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == "__main__":
    main()
