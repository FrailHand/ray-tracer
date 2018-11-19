from pyglet.gl import *
import constants


class Bench:
    def __init__(self):
        glClearColor(*constants.BACKGROUND_COLOR)

        self._axes = []

    def add_axis(self, axis):
        self._axes.append(axis)

    def update(self):
        for axis in self._axes:
            axis.trace_rays()

    def draw(self, window):

        window.clear()
        for axis in self._axes:
            axis.draw()
