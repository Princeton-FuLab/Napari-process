import napari
import glob
import os
from skimage import io
import imageio
import numpy as np
import cmap


#some parameter
output = "/Users/andyzjc/Downloads"
#color_map = cmap.Colormap('cet_cbl4').lut()
viewer = napari.Viewer()

file = "/Users/andyzjc/Dropbox (Princeton)/Polarizatino Engineered Aberration Robust Adaptive Light Sheet Microscope/Figures/Figure 3/Fig3_3/Data/Panel A/Panel B/take2_Collagen_200nmXStep_PEARLS_NBessel_NA0P6_na0p5_2p5mW_100ms_decon.tif"
image_1 = io.imread(file)
print(file)

layer1 = viewer.add_image(image_1,
                          colormap='inferno',
                          contrast_limits=[15212.796788194444, 136915.17109375], # manually determined
                          opacity=1, gamma=1.2,
                          rendering='attenuated_mip',
                          scale=(1.98, 1, 1),
                          blending='translucent')

viewer.dims.ndisplay = 3
viewer.camera.center = (1000, 550, 600)
viewer.camera.angles = (-52.96353268139426, 0.4813372491729526, 136.5367821617597)
viewer.camera.zoom = 0.45

# bounding box
layer1.bounding_box.visible = False
layer1.bounding_box.opacity = 0.5
layer1.bounding_box.line_color = [0,0,0,0]
layer1.bounding_box.line_color = [1, 1, 1, 1]

# scalebar
viewer.scale_bar.visible = False
viewer.scale_bar.position = 'bottom_left'
viewer.scale_bar.unit = "pixel"

# viewer.layers[0].bounding_box.line_color = [0,0,0,0]
# viewer.layers[0].bounding_box.line_color = [1,1,1,1]
# viewer.layers[0].bounding_box.opacity = 0.5

napari.run()