import pyglet
import math


class Blocks:
    def __init__(self):
        self.top = self.get_texture('texture/grass_top.png')
        self.side = self.get_texture('texture/grass_side.png')
        self.bottom = self.get_texture('texture/dir.png')

        self.vertex = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))
        self.texture_group = (self.side, self.side, self.side, self.side, self.bottom, self.top)
        self.batch = pyglet.graphics.Batch()

        self.block_len = 0
        self.block_sector = []
        self.new_block = []
        self.cube = []
        self.world = []

        self.faces = self.block_faces()

        self.generate_world()

    @staticmethod
    def get_texture(texture_file):
        texture = pyglet.image.load(texture_file)
        texture = texture.get_texture()
        return pyglet.graphics.TextureGroup(texture)

    def block_faces(self, nx=0, ny=0, nz=0):
        x, y, z = 0 + nx, 0 + ny, 0 + nz

        self.block_sector.append((x, y, z))

        return ((x + 1, y, z, x, y, z, x, y + 1, z, x + 1, y + 1, z),

                (x, y, z + 1, x + 1, y, z + 1, x + 1, y + 1, z + 1, x, y + 1, z + 1),

                (x, y, z, x, y, z + 1, x, y + 1, z + 1, x, y + 1, z),

                (x + 1, y, z + 1, x + 1, y, z, x + 1, y + 1, z, x + 1, y + 1, z + 1),

                (x, y, z, x + 1, y, z, x + 1, y, z + 1, x, y, z + 1),

                (x, y + 1, z + 1, x + 1, y + 1, z + 1, x + 1, y + 1, z, x, y + 1, z)
                )

    def create_block(self):
        self.cube = []
        for c in range(0, 6):
            self.cube.append(
                self.batch.add(4, pyglet.gl.GL_QUADS, self.texture_group[c], ('v3f', self.faces[c]), self.vertex))
        self.world.append(self.cube)

    def remove_block(self):
        if self.block_len >= 1:
            remove_sector = (round(self.new_block[0]) - 1, round(self.new_block[1]) - 2, round(self.new_block[2]) - 3)
            if remove_sector in self.block_sector:
                k = self.block_sector.index(remove_sector)
                for index in range(0, 6):
                    try:
                        self.world[k - 1][index].delete()
                    except Exception as error:
                        print(error)
                del self.world[k - 1]
                del self.block_sector[k]
                self.block_len -= 1
            del remove_sector

    def add_block(self):
        add_sector = (round(self.new_block[0]) - 1, round(self.new_block[1]) - 2, round(self.new_block[2]) - 3)
        if add_sector not in self.block_sector:
            self.block_len += 1
            self.faces = self.block_faces(nx=round(self.new_block[0]) - 1, ny=round(self.new_block[1]) - 2,
                                          nz=round(self.new_block[2]) - 3)
            self.create_block()
        del add_sector

    def generate_world(self):
        for x in range(-16, 16):
            for z in range(-16, 16):
                self.faces = self.block_faces(nx=x, ny=0, nz=z)
                self.create_block()

    def collision(self, px, py, pz):
        collision_sector = []
        collision_side = (round(px), round(py) - 2, round(pz) - 1)
        if collision_side in self.block_sector:
            del collision_side
            collision_sector.append(True)
        else:
            del collision_side
            collision_sector.append(False)

        collision_bottom = (round(px), round(py) - 3, round(pz) - 1)
        if collision_bottom in self.block_sector:
            del collision_bottom
            collision_sector.append(True)
        else:
            del collision_bottom
            collision_sector.append(False)

        return collision_sector


class Player:
    def __init__(self, pos=(0, 0, 0), rotation=(0, 0)):
        self.pos = list(pos)
        self.rotation = list(rotation)

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

    def update(self, dt, keys, block_situation):
        s = dt * 8

        rot_y = -self.rotation[1] / 180 * math.pi

        dx, dz = s * math.sin(rot_y), s * math.cos(rot_y)

        if keys[pyglet.window.key.W] and not block_situation[0]:
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
            i = 0
            while i < 2:
                self.pos[1] += s
                i += 1

        if keys[pyglet.window.key.LSHIFT] and not block_situation[1]:
            self.pos[1] -= s

        if not block_situation[1]:
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
        self.block_collision = (False, True)

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


if __name__ == '__main__':
    window = Window(width=900, height=600, caption='Minecraft in python', resizable=True)
    pyglet.app.run()
