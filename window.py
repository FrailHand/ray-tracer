import pyglet
from pyglet import gl
from pyglet.window import key
from bench import Bench


class Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(height=720, width=1280, resizable=True)

        self.set_caption('Ray Tracer')

        self.bench = Bench()

        pyglet.clock.schedule_interval(self.update, interval=1/30)

    def update(self, dt):
        self.bench.update()

    def on_draw(self):
        self.bench.draw(self)

