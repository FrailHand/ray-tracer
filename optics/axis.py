import numpy as np
from pyglet import gl
from pyglet import graphics
from sortedcontainers import SortedList

import constants
from optics.source import Source
from optics.ray import Ray


class Axis:
    def __init__(self, origin, direction, length):
        self.origin = np.atleast_1d(origin)
        self.length = length

        self.direction = np.atleast_1d(direction)
        assert (not all(self.direction == 0))
        self.direction = self.direction.astype(float) / np.linalg.norm(self.direction)

        self.end = self.origin + self.direction * self.length

        cos = self.direction[0]
        sin = self.direction[1]
        self.rotation_matrix = np.array([[cos, -sin], [sin, cos]])

        self.optics = SortedList(key=lambda x: x.position)
        self.rays = []

    def add_optics(self, optics):
        self.optics.add(optics)
        if optics.position > self.length - 100:
            self.set_length(optics.position + 100)

    def trace_rays(self):
        rays = []

        for optics in self.optics:
            for ray in rays:
                ray.go_through(optics)

            if isinstance(optics, Source):
                for new_ray in optics.rays:
                    rays.append(Ray(optics.position, new_ray))

        self.rays.clear()
        for ray in rays:
            ray.propagate(self.length)
            self.rays.append(ray.positions)

    def to_absolute_coordinates(self, coordinates):
        rotated = self.rotation_matrix.dot(coordinates)
        if coordinates.ndim > 1:
            return rotated + np.atleast_2d(self.origin).transpose()
        return rotated + self.origin

    def set_length(self, length):
        self.length = length
        self.end = self.origin + self.direction * self.length

    def draw(self):
        gl.glPushAttrib(gl.GL_ENABLE_BIT)

        gl.glLineStipple(*constants.AXIS_DASH)
        gl.glLineWidth(constants.AXIS_WIDTH)
        gl.glEnable(gl.GL_LINE_STIPPLE)

        gl.glColor3f(*constants.AXIS_COLOR)
        graphics.draw(2, gl.GL_LINES,
                      ('v2i', (*self.origin.astype(int), *self.end.astype(int)))
                      )

        gl.glPopAttrib()

        for ray in self.rays:
            gl.glLineWidth(constants.RAY_WIDTH)
            gl.glColor3f(*constants.RAY_COLOR)

            points = len(ray)
            ray_path = np.array(ray).transpose()
            ray_path = self.to_absolute_coordinates(ray_path)
            ray_path = np.reshape(ray_path.transpose(), -1).astype(int)
            graphics.draw(points, gl.GL_LINE_STRIP,
                          ('v2i', tuple(ray_path))
                          )

        for optic in self.optics:
            optic.draw()
