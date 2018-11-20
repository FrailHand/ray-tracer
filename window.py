import pyglet

from bench import Bench


class Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(height=720, width=1280, resizable=True)

        self.set_caption('Ray Tracer')

        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)

        self.bench = Bench()

        pyglet.clock.schedule_interval(self.update, interval=1/30)

    def update(self, dt):
        self.bench.update()

    def on_draw(self):
        self.bench.draw(self)

    def on_mouse_motion(self, x, y, dx, dy):
        self.bench.move_mouse(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        self.bench.mouse_click(self.keys[pyglet.window.key.LCTRL])

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.bench.mouse_drag(dx, dy)


