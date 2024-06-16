import napari
import glob
import os
from skimage import io
import imageio
import numpy as np
import cmap

fps = 30
video_path = 'Y:\Tian-Ming_Fu\Files_from_Janelia\LLS/20201209_LLS\Hela_CSII_mCherry_CAAX\Cell2/video/output_video_cell2.mp4'
image_path = 'Y:\Tian-Ming_Fu\Files_from_Janelia\LLS/20201209_LLS\Hela_CSII_mCherry_CAAX\Cell2/video/'
writer = imageio.get_writer(video_path, fps=fps)
viewer = napari.Viewer()
colormap = cmap.Colormap('hot').lut()

# single color
file_pattern = "Y:\Tian-Ming_Fu\Files_from_Janelia\LLS/20201209_LLS\Hela_CSII_mCherry_CAAX\Cell2\GPUdecon/*.tif"
tiff_files_1 = glob.glob(file_pattern)
tiff_files_1.sort()

max_int = 4000

# just show first image, show around
image_1 = io.imread(tiff_files_1[0])
layer1 = viewer.add_image(image_1, name='560', colormap=colormap, blending='translucent', rendering='mip',
                          contrast_limits=[50, max_int], opacity=1, gamma=0.5, scale=[1.98, 1, 1])
viewer.dims.ndisplay = 3
viewer.camera.zoom = 0.42
viewer.camera.center = (0, 500, 530)
layer1.bounding_box.visible = True
layer1.bounding_box.line_color = [1, 1, 1, 1]
layer1.bounding_box.opacity = 0.2

view_angle1 = np.linspace(start=-30, stop=30, num=150)
i = 0
for one_angle in view_angle1:
    viewer.camera.angles = (0, one_angle, 85)
    save_image = image_path + f'image_{i}.png'  # Change file extension if necessary
    frame = viewer.screenshot(path=save_image, size=[1008, 1008])  # Take a screenshot of the current view
    writer.append_data(frame)  # Add the screenshot to the video
    i += 1

view_angle2 = np.linspace(start=85, stop=265, num=90)
for one_angle in view_angle2:
    viewer.camera.angles = (0, 30, one_angle)
    save_image = image_path + f'image_{i}.png'  # Change file extension if necessary
    frame = viewer.screenshot(path=save_image, size=[1008, 1008])  # Take a screenshot of the current view
    writer.append_data(frame)  # Add the screenshot to the video
    i += 1

view_zoom = np.linspace(start=0.42, stop=2.3, num=300)
j = 0
for tiff_file_1 in tiff_files_1:
    image_1 = io.imread(tiff_file_1)
    # frame_corrected = (first_mean-bg) / (np.mean(image_1.reshape(-1)) - bg) * (image_1-bg)
    print(tiff_file_1)
    # print((first_mean-bg) / (np.mean(image_1.reshape(-1)) - bg))
    max_int = np.max(image_1.reshape(-1))
    layer1 = viewer.add_image(image_1, name='560', colormap=colormap,blending='translucent', rendering='mip',
                          contrast_limits=[50, max_int], opacity=1, gamma=0.5, scale=[1.98, 1, 1])

    viewer.dims.ndisplay = 3
    viewer.camera.zoom = view_zoom[j]
    viewer.camera.angles = (0, 30, 264)
    viewer.camera.center =

    layer1.bounding_box.visible = True
    layer1.bounding_box.line_color = [1, 1, 1, 1]
    layer1.bounding_box.opacity = 0.2

    save_image = image_path + f'image_{i}.png'  # Change file extension if necessary
    frame = viewer.screenshot(path=save_image, size=[1008, 1008])  # Take a screenshot of the current view
    writer.append_data(frame)  # Add the screenshot to the video
    viewer.layers.remove(layer1)
    i += 1
    j += 1

writer.close()
