import numpy as np
import pygame as pg
import math
class Player:
    def __init__(self):
        self.pos = np.array([0., 0.])
        self.angle = math.pi/4
        self.tilt = int(255 * 0.1)
        self.height = int(255 * 1.5)
        self.vel = 5
        self.vel_angle = 0.01

    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] :
           self.tilt += self.vel
        if keys[pg.K_DOWN] :
            self.tilt -= self.vel

        if keys[pg.K_LEFT]:
           self.angle -= self.vel_angle
        if keys[pg.K_RIGHT]:
            self.angle += self.vel_angle

        if keys[pg.K_q]:
           self.height += self.vel
        if keys[pg.K_z]:
            self.height -= self.vel

        if keys[pg.K_w]:
           self.pos[0] += self.vel * math.cos(self.angle)
           self.pos[1] += self.vel * math.sin(self.angle)

        if keys[pg.K_s]:
            self.pos[0] -= self.vel * math.cos(self.angle)
            self.pos[1] -= self.vel * math.sin(self.angle)

        if keys[pg.K_a]:
            self.pos[0] += self.vel * math.sin(self.angle)
            self.pos[1] -= self.vel * math.cos(self.angle)

        if keys[pg.K_d]:
            self.pos[0] -= self.vel * math.sin(self.angle)
            self.pos[1] += self.vel * math.cos(self.angle)





    def update(self):
        self.get_keys()
    def draw(self):
        pass
