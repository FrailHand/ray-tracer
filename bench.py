from pyglet.gl import *
import constants
import numpy as np

class Bench:
    def __init__(self):
        glClearColor(*constants.BACKGROUND_COLOR)

        self._axes = []

        self.highlighted = None
        self.selected = []

    def add_axis(self, axis):
        self._axes.append(axis)

    def update(self):
        for axis in self._axes:
            axis.trace_rays()

    def move_mouse(self, x, y):
        coord = np.array((x,y))
        nearest = None
        dist = -1
        for ax in self._axes:
            current = ax.distance(coord)
            if current >=0:
                if dist == -1 or current < dist:
                    dist = current
                    nearest = ax

        if nearest is not None:
            highlight = nearest.select(coord)
        else:
            highlight = None

        if self.highlighted is not None:
            if self.highlighted != highlight and self.highlighted not in self.selected:
                self.highlighted.color = self.highlighted.base_color
        self.highlighted = highlight
        if self.highlighted is not None and self.highlighted not in self.selected:
            self.highlighted.color = constants.HIGHLIGHT_COLOR

    def mouse_click(self, add_select):
        if not add_select:
            for elmt in self.selected:
                elmt.color = elmt.base_color
            self.selected.clear()

        if self.highlighted is not None and self.highlighted not in self.selected:
            self.highlighted.color = constants.SELECT_COLOR
            self.selected.append(self.highlighted)

    def mouse_drag(self, dx, dy):
        for object in self.selected:
            translate = object.axis.project(np.array((dx, dy)))
            object.position += translate

    def draw(self, window):

        window.clear()
        for axis in self._axes:
            axis.draw()
