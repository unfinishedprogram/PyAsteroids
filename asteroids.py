import math
import pygame
import pygame.key
import random
import pygame.gfxdraw

# Dynamic general game object class
from pygame.constants import *

framerate = 120
frametime = 1000/framerate


class Display(object):

    def __init__(self):
        self.screen_res = (1600, 1200)
        self.scale = 2
        self.clock = pygame.time.Clock()
        pygame.init()
        pygame.display.set_caption("Python Asteroids")
        self.screen = pygame.display.set_mode(self.screen_res)

    def draw(self, game_object):
        vectors_to_draw = []
        for vert in game_object.verts:
            rotated = vert.rotate(game_object.direction)

            xpos = (game_object.pos.x + rotated.x) * self.scale
            ypos = (game_object.pos.y + rotated.y) * self.scale
            vectors_to_draw.append(pygame.Vector2(xpos, ypos))
        pygame.gfxdraw.aapolygon(self.screen, vectors_to_draw, (255, 255, 255))
    def draw_point(self, vector):
        pygame.draw.circle(self.screen, (255, 255, 255), (vector.x * self.scale, vector.y * self.scale), self.scale/2)

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
        return self

    def invert(self):
        self.x *= -1
        self.y *= -1
        return self

    def dot_product(self, vec2):
        self.x *= vec2.x
        self.y *= vec2.y
        return self

    def multiply(self, factor):
        return vector2(self.x * factor, self.y * factor)

    def rotate(self, rads):
        x = self.x * math.cos(rads) - self.y * math.sin(rads)
        y = self.x * math.sin(rads) + self.y * math.cos(rads)
        return vector2(x, y)

    def diff(self, vector):
        return vector2(self.x-vector.x, self.y-vector.y)

    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalized(self):
        mag = self.magnitude()
        return vector2(self.x/mag, self.y/mag)


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
        self.asteroids = [Asteroid(2, 10)]
        self.bullets = []
        self.turn_speed = 5  # degrees per frame
        self.asteroid_delay = 3
        self.display = Display()
        self.framerate = 60
        self.clock = pygame.time.Clock()
        self.bulletDelay = 200 # ms
        self.bulletTimer = 0

    def spawnAsteroid(self):
        angle = toRad(random.random() * 360)
        position = vector2(math.cos(angle), math.sin(angle)).invert()

        self.asteroids.append(Asteroid(position, random.random()*20))




    def handle_colisions(self):
        for bullet in self.bullets:
            for asteroid in self.asteroids:
                if bullet.pos.diff(asteroid.pos).mag() < 20:
                    pass

    def area(self, tri):
        return abs((tri[0].x * (tri[1].y - tri[2].y) + tri[1].x * (tri[2].y - tri[0].y) + tri[2].x * (tri[0].y - tri[1].y)) / 2)

    def detect_point_in_triangle(self, point, triangle):
        pass






    def step(self):
        self.clock.tick_busy_loop(120)
        self.bulletTimer -= frametime;
        print(len(self.bullets))
        if pygame.key.get_focused():
            if pygame.key.get_pressed()[K_UP]:
                self.player.apply_thrust()
            if pygame.key.get_pressed()[K_RIGHT]:
                self.player.turn(1)
            if pygame.key.get_pressed()[K_LEFT]:
                self.player.turn(-1)
            if pygame.key.get_pressed()[K_SPACE]:
                if self.bulletTimer <= 0:
                    self.bulletTimer = self.bulletDelay
                    self.bullets.append(Bullet(self.player.pos.copy(), self.player.direction))


        self.display.screen.fill((0, 0, 0))

        for asteroid in self.asteroids:
            if not asteroid.step():
                if(asteroid.size > 5):
                    self.asteroids.append(Asteroid(asteroid.pos, asteroid.size / 2))
                    self.asteroids.append(Asteroid(asteroid.pos, asteroid.size / 2))
                self.asteroids.remove(self.asteroids.index(asteroid))


        for i in range(len(self.bullets)):
            try:
                if not self.bullets[i].step():
                    self.bullets.remove(self.bullets.index(self.bullets[i]))
                else:
                    pass
                    if -10 > self.bullets[i].pos.x or 810 < self.bullets[i].pos.x or -10 > self.bullets[i].pos.y or 610 < self.bullets[i].pos.y:
                        self.bullets.remove(self.bullets[i])
                        i -= 1
            except: pass


        if self.player.step() == "gameOver":
            return "gameOver"
        self.display.draw(self.player)

        for asteroid in self.asteroids:
            self.display.draw(asteroid)

        for bullet in self.bullets:
            self.display.draw_point(bullet.pos)
class Player(gameObject):
    def __init__(self):
        self.pos = vector2(200, 400)
        self.velocity = vector2(0, 0)
        self.direction = toRad(180+90)
        self.turn_speed = math.pi/(360*2)
        self.thrust_power = 0.02

        self.verts = [
            vector2(7, 0),
            vector2(-4, -4),
            vector2(0, 0),
            vector2(-4, 4),
            vector2(7, 0)
        ]


    def step(self):
        self.apply_velocity()
        self.apply_friction()

    def apply_thrust(self):
        thrust_vector = vector2(math.cos(self.direction) * self.thrust_power * frametime / 20, math.sin(self.direction) * self.thrust_power * frametime / 20)
        self.velocity.add(thrust_vector)

    def apply_friction(self):
        self.velocity.x = self.velocity.x * (1 - 0.002 * frametime)
        self.velocity.y = self.velocity.y * (1 - 0.002 * frametime)

    def turn(self, dir):  # dir from 1 to -1 for right and left
        self.direction += dir * self.turn_speed * frametime

    def apply_velocity(self):
        self.pos.add(self.velocity.multiply(frametime))


class Asteroid(gameObject):
    def __init__(self, pos, size):
        self.size = size
        self.pos = vector2(200, 200)
        self.velocity = vector2(0, 1)
        self.verts = self.gen_verts(16, size)
        self.direction = 0


    def gen_verts(self, vertCount, size):
        verts = []
        for i in range(vertCount):
            amplitude = ((2 + random.random()) * size)
            current_rad = (2 * math.pi / vertCount * i)
            verts.append(vector2(math.cos(current_rad) * amplitude, math.sin(current_rad) * amplitude))

        return verts
    def step(self):
        self.pos.add(self.velocity.multiply(frametime/100))
        return True

class Bullet(gameObject):
    def __init__(self, pos, direction):
        self.velocity = vector2 (math.cos(direction), math.sin(direction))
        self.pos = pos
        self.direction = direction
    def step(self):
        self.pos.add(self.velocity.multiply(frametime/2))
        return True


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
