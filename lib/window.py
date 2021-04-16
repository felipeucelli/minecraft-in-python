import pyglet
from .blocks import Blocks
from .player import Player


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_minimum_size(300, 200)
        pyglet.gl.glClearColor(0.5, 0.7, 1, 1)
        pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)

        self.mouse_lock = False
        self.block_collision = [False, True, False]

        self.blocks = Blocks()
        self.player = Player((-0.5, 3, 0), (-30, 0))

    def gl_push(self, pos):
        pyglet.gl.glPushMatrix()
        rotation = self.player.rotation
        pyglet.gl.glRotatef(-rotation[0], 1, 0, 0)
        pyglet.gl.glRotatef(-rotation[1], 0, 1, 0)
        pyglet.gl.glTranslatef(-pos[0], -pos[1], -pos[2], )

    @staticmethod
    def set_gl_projection():
        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()

    @staticmethod
    def set_gl_model():
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
        pyglet.gl.glLoadIdentity()

    def set3d(self):
        self.set_gl_projection()
        pyglet.gl.gluPerspective(70, self.width / self.height, 0.05, 1000)
        self.set_gl_model()

    def relative_pos(self):
        if 65 > self.player.rotation[1] >= 0 or 0 < self.player.rotation[1] > 300:
            self.blocks.new_block = self.player.pos

        if 65 < self.player.rotation[1] < 130:
            self.blocks.new_block = (self.player.pos[0] - 2, self.player.pos[1], self.player.pos[2] + 2.5)

        if 130 < self.player.rotation[1] < 240:
            self.blocks.new_block = (self.player.pos[0] + 1, self.player.pos[1], self.player.pos[2] + 5)

        if 240 < self.player.rotation[1] < 300:
            self.blocks.new_block = (self.player.pos[0] + 3, self.player.pos[1], self.player.pos[2] + 2)

    def mouse_status(self, status):
        self.set_exclusive_mouse(status)

    def update(self, dt):
        self.player.update(dt, self.keys, self.block_collision)
        self.block_collision = self.blocks.collision(px=self.player.pos[0], py=self.player.pos[1],
                                                     pz=self.player.pos[2])

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_lock:
            self.player.mouse_movement(dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == 1:
            self.blocks.add_block()
        else:
            self.blocks.remove_block()

    def on_key_press(self, key, key_mod):
        if key == pyglet.window.key.ESCAPE:
            self.close()
        if key == pyglet.window.key.E:
            self.mouse_lock = not self.mouse_lock
            self.mouse_status(self.mouse_lock)

    def on_draw(self):
        self.clear()
        self.set3d()
        self.gl_push(self.player.pos)
        self.blocks.batch.draw()
        pyglet.gl.glPopMatrix()
        self.relative_pos()
