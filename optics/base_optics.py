from abc import ABCMeta

import numpy as np
from pyglet import gl
from pyglet import graphics

import constants


class BaseOptics(metaclass=ABCMeta):
    def __init__(self, position, axis):
        self.position = position
        self.axis = axis
        self.propagation_matrix = np.eye(2)

    @property
    def coordinates(self):
        return np.atleast_1d((self.position, 0))

    def draw(self, color):
        base = self.coordinates
        perp = np.atleast_1d((0, 1))
        bottom = base - constants.OBJECT_HALF_HEIGHT * perp
        top = base + constants.OBJECT_HALF_HEIGHT * perp

        bottom = self.axis.to_absolute_coordinates(bottom)
        top = self.axis.to_absolute_coordinates(top)

        gl.glLineWidth(4)
        gl.glColor3f(*color)

        graphics.draw(2, gl.GL_LINES,
                      ('v2i', (*bottom.astype(int), *top.astype(int)))
                      )
