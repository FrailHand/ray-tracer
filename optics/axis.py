import numpy as np
from pyglet import gl
from pyglet import graphics

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

        self.optics = []
        self.rays = []

    def add_optics(self, optics):
        self.optics.append(optics)
        if optics.position > self.length - 100:
            self.set_length(optics.position + 100)

    def trace_rays(self):
        rays = []

        sorted_optics = sorted(self.optics, key=lambda x: x.position)
        for optics in sorted_optics:
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

    def to_relative_coordinates(self, coordinates):
        rotated = self.rotation_matrix.transpose().dot(coordinates)
        if coordinates.ndim > 1:
            return rotated - np.atleast_2d(self.origin).transpose()
        return rotated - self.origin

    def distance(self, coordinates):
        relative = self.to_relative_coordinates(coordinates)
        if 0 < relative[0] < self.length:
            dist = abs(relative[1])
            if dist > constants.OBJECT_HALF_HEIGHT:
                return -1
            return dist
        else:
            return -1

    def select(self, coordinates):
        relative = self.to_relative_coordinates(coordinates)
        selector = relative[0]
        sorted_optics = sorted(self.optics, key=lambda x: x.position)

        nearest = None
        dist = -1
        for optic in sorted_optics:
            current = abs(optic.position - selector)
            if current < constants.OBJECT_HALF_HEIGHT:
                if dist == -1 or current < dist:
                    dist = current
                    nearest = optic
        return nearest

    def set_length(self, length):
        self.length = length
        self.end = self.origin + self.direction * self.length

    def project(self, coord):
        return self.to_relative_coordinates(coord)[0]

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
