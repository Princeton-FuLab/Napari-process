import napari
import glob
import os
from skimage import io
import imageio
import numpy as np
import cmap
from scipy import stats

output_path = '/Users/andyzjc/Dropbox (Princeton)/Polarizatino Engineered Aberration Robust Adaptive Light Sheet Microscope/Figures/Figure 5/Fig5_4/Data/Data/dual-color'
nucleus_cmap = cmap.Colormap('magenta').lut()
membrane_cmap = cmap.Colormap('green').lut()

nchannels = [488, 560]
file_pattern = "/Users/andyzjc/Dropbox (Princeton)/Polarizatino Engineered Aberration Robust Adaptive Light Sheet Microscope/Figures/Figure 5/Fig5_4/Data/Data/dual-color/{}/*.tif"
channels = [file_pattern.format(i) for i in nchannels]
tiff_files_1 = glob.glob(channels[0])
tiff_files_1.sort()
tiff_files_2 = glob.glob(channels[1])
tiff_files_2.sort()
assert len(tiff_files_1) == len(tiff_files_2), "The number of TIFF files in each folder must be the same."

viewer = napari.Viewer()
viewer.dims.ndisplay = 3

# photo bleach correction based on first stack background and average
first_image_488 = io.imread(tiff_files_1[0])
# layer1 = viewer.add_image(first_image_488, name='488', contrast_limits=[0, np.max(first_image_488)])
# viewer.dims.ndisplay = 3
# viewer.camera.angles = (0, 0, 90)
# viewer.camera.center = (0, 300, 530)
# viewer.camera.zoom = 2.5
# frame = viewer.screenshot(size=[1008, 1008])
first_mean488 = np.mean(first_image_488.reshape(-1))
first_max488 = np.max(first_image_488.reshape(-1))
bg488 = 20 # estimated based on mip
# viewer.layers.remove(layer1)

first_image_560 = io.imread(tiff_files_2[0])
# layer2 = viewer.add_image(first_image_560, name='560', contrast_limits=[0, np.max(first_image_560)])
# viewer.dims.ndisplay = 3
# viewer.camera.angles = (0, 0, 90)
# viewer.camera.center = (0, 300, 530)
# viewer.camera.zoom = 2.5
# frame = viewer.screenshot(size=[1008, 1008])
first_mean560 = np.mean(first_image_560.reshape(-1))
first_max560 = np.max(first_image_560.reshape(-1))
bg560 = 2 # estimated based on mip
# viewer.layers.remove(layer2)

# overview
# viewer.scale_bar.visible = False
# viewer.scale_bar.position = 'bottom_left'
# viewer.scale_bar.unit = "pixel"
# viewer.camera.center = (266.31, 511.5, 539.5)
# viewer.camera.angles = (-96.30760603888365, 20.736489465576195, 78.97015296715203)
# viewer.camera.zoom = 0.57
# viewer.layers[0].contrast_limits = [60,5000]
# viewer.layers[0].bounding_box.line_color = [0,0,0,0]
# viewer.layers[0].bounding_box.line_color = [1,1,1,1]
# viewer.layers[0].bounding_box.points = False

# yz overview
# viewer.camera.angles = (0.0, 0.0, 90.0)
# viewer.camera.center = (0.0, 263.90990127723853, 513.1285626575371)
# viewer.camera.zoom = 0.577
# viewer.layers[0].contrast_limits= [80,3100]

# crop with a shape
# shape_coordinate = [[  24.03321371,  567.        ,   81.09592696],
#         [ 239.67495914,  567.        ,   81.09592696],
#         [ 239.67495914,  567.        , 1029.33750642],
#         [  24.03321371,  567.        , 1029.33750642]]
# crop_shape = viewer.add_shapes(data=shape_coordinate, ndim=3,shape_type='rectangle',)

i = 0
for tiff_file_1, tiff_file_2 in zip(tiff_files_1, tiff_files_2):
    print(tiff_file_1)
    print(tiff_file_2)

    # image_1 = io.imread(tiff_file_1)
    # layer1 = viewer.add_image(image_1, name='488', contrast_limits=[0, np.max(image_1)])
    # viewer.dims.ndisplay = 3
    # viewer.camera.angles = (0, 0, 90)
    # viewer.camera.center = (0, 300, 530)
    # viewer.camera.zoom = 2.5
    # frame488 = viewer.screenshot(size=[1008, 1008])  # Take a screenshot of the current view
    # frame488_corrected = first_mean488 / np.mean(frame488.reshape(-1)) * frame488
    # viewer.layers.remove(layer1)
    #
    # image_2 = io.imread(tiff_file_2)
    # layer2 = viewer.add_image(image_2, name='560', contrast_limits=[0, np.max(image_2)])
    # viewer.dims.ndisplay = 3
    # viewer.camera.angles = (0, 0, 90)
    # viewer.camera.center = (0, 300, 530)
    # viewer.camera.zoom = 2.5
    # frame560 = viewer.screenshot(size=[1008, 1008])  # Take a screenshot of the current view
    # frame560_corrected = first_mean560 / np.mean(frame560.reshape(-1)) * frame560
    # viewer.layers.remove(layer2)

    # image_1 = io.imread(tiff_file_1)
    # frame488_corrected = first_mean488 / np.mean(image_1.reshape(-1)) * image_1
    # print(first_mean488 / np.mean(image_1.reshape(-1)))
    #
    # image_2 = io.imread(tiff_file_2)
    # frame560_corrected = first_mean560 / np.mean(image_2.reshape(-1)) * image_2
    # print(first_mean560 / np.mean(image_2.reshape(-1)))

    image_1 = io.imread(tiff_file_1)
    frame488_corrected = (first_mean488) / (np.mean(image_1.reshape(-1))) * (image_1)
    print((first_mean488) / (np.mean(image_1.reshape(-1))))

    image_2 = io.imread(tiff_file_2)
    frame560_corrected = (first_mean560-bg560) / (np.mean(image_2.reshape(-1))-bg560) * (image_2-bg560)
    print((first_mean560-bg560) / (np.mean(image_2.reshape(-1))-bg560))

    layer1 = viewer.add_image(frame488_corrected, name='488', colormap=membrane_cmap,blending='translucent',
                              contrast_limits=[np.min(frame488_corrected), first_max488], opacity=1, gamma=0.5,scale=(1.98, 1, 1))
    layer2 = viewer.add_image(frame560_corrected, name='560', colormap=nucleus_cmap,blending='additive',
                              contrast_limits=[np.min(frame560_corrected), first_max560], opacity=1, gamma=0.5,scale=(1.98, 1, 1))
    napari.run()
    viewer.dims.ndisplay = 3
    viewer.camera.angles = (0, 0, 90)
    viewer.camera.center = (0, 300, 530)
    viewer.camera.zoom = 2.5

    # napari.run()
    save_image = output_path + f'depiction_image_{i}.png'  # Change file extension if necessary-
    frame = viewer.screenshot(path=save_image, size=[1008, 1008])  # Take a screenshot of the current view
    viewer.layers.remove(layer1)
    viewer.layers.remove(layer2)
    i += 1

# first image, zoomed out
# viewer.camera.center = (0, 400, 530)
# viewer.camera.zoom = 0.8