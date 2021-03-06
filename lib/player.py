import pyglet
import math
from .blocks import Blocks


class Player:
    def __init__(self, pos=(0, 0, 0), rotation=(0, 0)):
        self.pos = list(pos)
        self.rotation = list(rotation)
        self.flight = False

        self.blocks = Blocks()

    def mouse_movement(self, dx, dy):
        dx /= 8
        dy /= 8

        self.rotation[0] += dy
        self.rotation[1] -= dx

        if self.rotation[1] > 360:
            self.rotation[1] = 0
        elif self.rotation[1] < 0:
            self.rotation[1] = 360

        if self.rotation[0] > 90:
            self.rotation[0] = 90
        elif self.rotation[0] < -90:
            self.rotation[0] = -90

    def keys_press(self, keys, dx, dz, s, block_situation, vision_direction):
        i = 0
        jump_limit = 2
        if keys[pyglet.window.key.W]:
            jump_limit = 3
            if not block_situation[0] or vision_direction[2] == 'Z':
                self.pos[0] += dx
            if not block_situation[0] or vision_direction[2] == 'X':
                self.pos[2] -= dz

        if keys[pyglet.window.key.S]:
            if not block_situation[0] or vision_direction[2] == 'Z':
                self.pos[0] -= dx
            if not block_situation[0] or vision_direction[2] == 'X':
                self.pos[2] += dz

        if keys[pyglet.window.key.A]:
            if not block_situation[0] or vision_direction[2] == 'X':
                self.pos[0] -= dz
            if not block_situation[0] or vision_direction[2] == 'Z':
                self.pos[2] -= dx

        if keys[pyglet.window.key.D]:
            if not block_situation[0] or vision_direction[2] == 'X':
                self.pos[0] += dz
            if not block_situation[0] or vision_direction[2] == 'Z':
                self.pos[2] += dx

        if keys[pyglet.window.key.SPACE]:
            if not self.flight:
                while i < jump_limit:
                    self.pos[1] += 0.1
                    i += 1
            else:
                self.pos[1] += s

        if keys[pyglet.window.key.LSHIFT] and not block_situation[1]:
            self.pos[1] -= s

        if not block_situation[1] and not self.flight:
            self.pos[1] -= s

        if keys[pyglet.window.key.TAB]:
            self.flight = not self.flight

    def update(self, dt, keys, block_situation, vision_direction):
        s = dt * 8

        rot_y = -self.rotation[1] / 180 * math.pi

        dx, dz = s * math.sin(rot_y), s * math.cos(rot_y)

        self.keys_press(keys=keys, dx=dx, dz=dz, s=s,
                        block_situation=block_situation, vision_direction=vision_direction)
