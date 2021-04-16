import pyglet


class Blocks:
    def __init__(self):
        self.top = self.get_texture('lib/texture/grass_top.png')
        self.side = self.get_texture('lib/texture/grass_side.png')
        self.bottom = self.get_texture('lib/texture/dir.png')

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
                    self.world[k - 1][index].delete()
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
