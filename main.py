import pyglet
from lib.window import Window

if __name__ == '__main__':
    window = Window(width=900, height=600, caption='Minecraft in python', resizable=True)
    pyglet.app.run()
