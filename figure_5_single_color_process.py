import napari
import glob
import os
from skimage import io
import imageio
import numpy as np
import cmap


#some parameter
output = "/Users/andyzjc/Downloads"
color_map = cmap.Colormap('hot').lut()
viewer = napari.Viewer()

file = "/Users/andyzjc/Dropbox (Princeton)/Polarizatino Engineered Aberration Robust Adaptive Light Sheet Microscope/Figures/Figure 5/Fig5_4/Data/Data/single-color/decon/560_5_CamB_ch0_CAM1_stack0299_560nm_3941829msec_0026035961msecAbs_000x_000y_000z_0000t_decon.tif"
image_1 = io.imread(file)
print(file)

layer1 = viewer.add_image(image_1,
                          colormap=color_map,
                          contrast_limits=[50, 2000], # manually determined
                          opacity=1, gamma=0.5,
                          rendering='mip',
                          scale=(1.98, 1, 1),
                          blending='translucent')
viewer.scale_bar.visible = False
viewer.scale_bar.position = 'bottom_left'
viewer.scale_bar.unit = "pixel"

# bounding box
layer1.bounding_box.visible = False
layer1.bounding_box.line_color = [1, 1, 1, 1]
layer1.bounding_box.opacity = 0.5

# viewer.layers[0].bounding_box.line_color = [0,0,0,0]
# viewer.layers[0].bounding_box.line_color = [1,1,1,1]
# viewer.layers[0].bounding_box.opacity = 0.5

napari.run()
# overview
viewer.camera.angles = (65, -60, 116)
viewer.camera.center = (250, 511.5, 514.0)
viewer.camera.zoom = 0.5
save_image = output + 'overview_mip.png'  # Change file extension if necessary-
frame = viewer.screenshot(path=save_image, size=[1008, 1008])  # Take a screenshot of the current view

# XY view
viewer.camera.angles = (0.0, 0.0, 90.0)
viewer.camera.center = (0.0, 511.5, 514.0)
viewer.camera.zoom = 0.7
viewer.layers[0].contrast_limits = [20,1700]
save_image = output + 'xy_mip.png'  # Change file extension if necessary-
frame = viewer.screenshot(path=save_image, size=[1008, 1008])  # Take a screenshot of the current view

# XY view tilted
viewer.camera.angles = (-141.63497427428373, -12.157949701378651, 72.40760687552508)
viewer.camera.center = (400.0, 900.0, 300.0)
viewer.camera.zoom = 1.9

# XZ view, need to rotate axis
viewer.camera.angles = (0.0, 0.0, 90.0)
viewer.camera.center = (0.0, 246.51, 511.5)
viewer.camera.zoom = 0.7
viewer.layers[0].contrast_limits = [20,1700]
save_image = output + 'xz_mip.png'  # Change file extension if necessary-
frame = viewer.screenshot(path=save_image, size=[1008, 1008])  # Take a screenshot of the current view

napari.run()
