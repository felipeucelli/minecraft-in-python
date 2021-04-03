import pyglet
import math


class Blocks:
    def __init__(self):
        self.top = self.get_texture('texture/grass_top.png')
        self.side = self.get_texture('texture/grass_side.png')
        self.bottom = self.get_texture('texture/dir.png')

        self.vertex = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))
        self.texture_group = (self.side, self.side, self.side, self.side, self.bottom, self.top)
        self.faces = self.block_faces()
        self.batch = pyglet.graphics.Batch()
        self.create_block()

    @staticmethod
    def get_texture(texture_file):
        texture = pyglet.image.load(texture_file)
        texture = texture.get_texture()
        return pyglet.graphics.TextureGroup(texture)

    @staticmethod
    def block_faces():
        x, y, z = 0, 0, -1

        return ((x + 1, y, z, x, y, z, x, y + 1, z, x + 1, y + 1, z),

                (x, y, z + 1, x + 1, y, z + 1, x + 1, y + 1, z + 1, x, y + 1, z + 1),

                (x, y, z, x, y, z + 1, x, y + 1, z + 1, x, y + 1, z),

                (x + 1, y, z + 1, x + 1, y, z, x + 1, y + 1, z, x + 1, y + 1, z + 1),

                (x, y, z, x + 1, y, z, x + 1, y, z + 1, x, y, z + 1),

                (x, y + 1, z + 1, x + 1, y + 1, z + 1, x + 1, y + 1, z, x, y + 1, z)
                )

    def create_block(self):
        for c in range(0, 6):
            self.batch.add(4, pyglet.gl.GL_QUADS, self.texture_group[c], ('v3f', self.faces[c]), self.vertex)


class Player:
    def __init__(self, pos=(0, 0, 0), rotation=(0, 0)):
        self.pos = list(pos)
        self.rotation = list(rotation)

    def mouse_movement(self, dx, dy):
        dx /= 8
        dy /= 8

        self.rotation[0] += dy
        self.rotation[1] -= dx

        if self.rotation[0] > 90:
            self.rotation[0] = 90
        elif self.rotation[0] < -90:
            self.rotation[0] = -90

    def update(self, dt, keys):
        s = dt * 8

        rot_y = -self.rotation[1] / 180 * math.pi

        dx, dz = s * math.sin(rot_y), s * math.cos(rot_y)

        if keys[pyglet.window.key.W]:
            self.pos[0] += dx
            self.pos[2] -= dz

        if keys[pyglet.window.key.S]:
            self.pos[0] -= dx
            self.pos[2] += dz

        if keys[pyglet.window.key.A]:
            self.pos[0] -= dz
            self.pos[2] -= dx

        if keys[pyglet.window.key.D]:
            self.pos[0] += dz
            self.pos[2] += dx

        if keys[pyglet.window.key.SPACE]:
            self.pos[1] += s

        if keys[pyglet.window.key.LSHIFT]:
            self.pos[1] -= s


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

        self.blocks = Blocks()
        self.player = Player((0.5, 1.5, 1.5), (-30, 0))

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

    def mouse_status(self, status):
        self.set_exclusive_mouse(status)

    def update(self, dt):
        self.player.update(dt, self.keys)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_lock:
            self.player.mouse_movement(dx, dy)

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


if __name__ == '__main__':
    window = Window(width=400, height=300, caption='Minecraft in python', resizable=True)
    pyglet.app.run()
