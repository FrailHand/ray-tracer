import pyglet

import window
from optics import thin_lens, source, axis

win = window.Window()

ax = axis.Axis((0, 360), (1, 0), 1280)

light = source.Source(50, ax)
light.add_ray(50, 0)
light.add_ray(50, -20)
light.add_ray(0, 10)
light.add_ray(0, -10)

lens = thin_lens.ThinLens(300, ax, 100)
ax.add_optics(lens)
lens = thin_lens.ThinLens(750, ax, 150)
lens.selected = True
ax.add_optics(lens)

ax.add_optics(light)

win.bench.add_axis(ax)

pyglet.app.run()
