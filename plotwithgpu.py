from vispy import app, scene
import numpy as np


def plsplotgpu(Z):
    Z = [Z]
    Z = np.reshape(Z, (20, 99))
    canvas = scene.SceneCanvas(keys='interactive', bgcolor='w')
    view = canvas.central_widget.add_view()
    view.camera = scene.TurntableCamera(up='z', fov=60)

    p1 = scene.visuals.SurfacePlot(z=Z, color=(0.3, 0.3, 1, 1))

    view.add(p1)

    xax = scene.Axis(pos=[[-0.5, -0.5], [0.5, -0.5]], tick_direction=(0, -1),
                     font_size=16, axis_color='k', tick_color='k', text_color='k',
                     parent=view.scene)
    xax.transform = scene.STTransform(translate=(0, 0, -0.2))

    yax = scene.Axis(pos=[[-0.5, -0.5], [-0.5, 0.5]], tick_direction=(-1, 0),
                     font_size=16, axis_color='k', tick_color='k', text_color='k',
                     parent=view.scene)
    yax.transform = scene.STTransform(translate=(0, 0, -0.2))

    canvas.show()
    app.run()
