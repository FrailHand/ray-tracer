from optics.base_optics import BaseOptics
import numpy as np

import constants


class Source(BaseOptics):
    def __init__(self, position, axis, visible=True):
        super().__init__(position, axis)
        self.visible = visible
        self.rays = []

    def draw(self):
        if self.visible:
            super().draw(constants.SOURCE_COLOR)

    def add_ray(self, height, angle):
        angle = np.deg2rad(angle)
        ray = np.array((height, angle))
        self.rays.append(ray)
