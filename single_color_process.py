import napari
import glob
import os
from skimage import io
import imageio
import numpy as np
import cmap

fps = 30
video_path = 'Z:\Tian-Ming_Fu\Files_from_Janelia\LLS/20201209_LLS\Hela_CSII_mCherry_CAAX\Cell2/video/output_video_cell2.mp4'
image_path = 'Z:\Tian-Ming_Fu\Files_from_Janelia\LLS/20201209_LLS\Hela_CSII_mCherry_CAAX\Cell2/video/'
writer = imageio.get_writer(video_path, fps=fps)
viewer = napari.Viewer()
colormap = cmap.Colormap('magenta').lut()

#cell3_cont
file_pattern = "Z:\Tian-Ming_Fu\Files_from_Janelia\LLS/20201209_LLS\Hela_CSII_mCherry_CAAX\Cell2\GPUdecon/*.tif"
tiff_files_1 = glob.glob(file_pattern)
tiff_files_1.sort()

# viewing
view_angle = np.linspace(start=-30, stop=30, num=300)

# photo bleach correction based on first stack background and average
first_image = io.imread(tiff_files_1[0])
first_mean = np.mean(first_image.reshape(-1))
first_max = np.max(first_image.reshape(-1))
bg = 2

i = 0
for tiff_file_1 in tiff_files_1:
    image_1 = io.imread(tiff_file_1)
    frame_corrected = (first_mean-bg) / (np.mean(image_1.reshape(-1)) - bg) * (image_1-bg)
    print(tiff_file_1)
    print((first_mean-bg) / (np.mean(image_1.reshape(-1)) - bg))

    layer1 = viewer.add_image(frame_corrected, name='560', colormap=colormap,
                          contrast_limits=[0, first_max/2], opacity=1, gamma=0.85, scale=[1.85, 1, 1])

    viewer.dims.ndisplay = 3
    viewer.camera.zoom = 0.42
    viewer.camera.angles = (0, view_angle[i], 85)
    viewer.camera.center = (0, 500, 530)

    layer1.bounding_box.visible = True
    layer1.bounding_box.line_color = [1, 1, 1, 1]
    layer1.bounding_box.opacity = 0.2

    save_image = image_path + f'image_{i}.png'  # Change file extension if necessary
    frame = viewer.screenshot(path=save_image, size=[1008, 1008])  # Take a screenshot of the current view
    writer.append_data(frame)  # Add the screenshot to the video
    viewer.layers.remove(layer1)
    i += 1
writer.close()
