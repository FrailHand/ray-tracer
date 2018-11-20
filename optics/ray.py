import numpy as np


class Ray:
    def __init__(self, position, vector):
        self.position = position
        self.vector = np.atleast_1d(vector)
        self.positions = [self.coordinates]

    @property
    def coordinates(self):
        return np.atleast_1d((self.position, self.vector[0]))

    def go_through(self, optics):
        # propagate through air to the optics
        self.propagate(optics.position)

        # propagate through the optics
        matrix = optics.propagation_matrix
        self.vector = matrix.dot(self.vector)

        # save current position
        self.positions.append(self.coordinates)

    def propagate(self, target):
        matrix = np.eye(2)
        matrix[0, 1] = target - self.position
        self.vector = matrix.dot(self.vector)
        self.position = target

        self.positions.append(self.coordinates)
