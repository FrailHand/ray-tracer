from optics.base_optics import BaseOptics
import numpy as np
from pyglet import graphics, gl


class ThinLens(BaseOptics):
    def __init__(self, position, axis, focal_length):
        super().__init__(position, axis)
        self.focal_length = focal_length

        self.propagation_matrix[1, 0] = -1 / self.focal_length

    def draw(self):
        color = (0, 0.5, 0.65)
        super().draw(color)

        focal_1 = self.axis.to_absolute_coordinates(
            np.atleast_1d((self.position + self.focal_length, 0)))
        focal_2 = self.axis.to_absolute_coordinates(
            np.atleast_1d((self.position - self.focal_length, 0)))

        gl.glColor3f(*color)
        gl.glPointSize(10)
        graphics.draw(2, gl.GL_POINTS,
                      ('v2i', (*focal_1.astype(int), *focal_2.astype(int)))
                      )
