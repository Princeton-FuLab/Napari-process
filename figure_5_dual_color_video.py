import napari
import glob
import os
from skimage import io
import imageio
import numpy as np
import cmap

# video setting
fps = 30
video_path = 'Y:\Tian-Ming_Fu\Files_from_Janelia\LLS/20201209_LLS\LLCPK1_ER-mEmerald-H2B-mCherry/video/output_video_cell3_3.mp4'
image_path = 'Y:\Tian-Ming_Fu\Files_from_Janelia\LLS/20201209_LLS\LLCPK1_ER-mEmerald-H2B-mCherry/video/'
writer = imageio.get_writer(video_path, fps=fps)
nucleus_cmap = cmap.Colormap('magenta').lut()
membrane_cmap = cmap.Colormap('green').lut()
viewer = napari.Viewer()

# readin data, cell3
nchannels = [488, 560]
file_pattern = "Y:\Tian-Ming_Fu\Files_from_Janelia\LLS/20201209_LLS\LLCPK1_ER-mEmerald-H2B-mCherry\Cell3\GPUdecon/{}/*.tif"
channels = [file_pattern.format(i) for i in nchannels]
cell3_488 = glob.glob(channels[0])
cell3_488.sort()
cell3_560 = glob.glob(channels[1])
cell3_560.sort()
assert len(cell3_488) == len(cell3_560), "The number of TIFF files in each folder must be the same."

# cell3 viewing
view_angle = np.linspace(start=0, stop=45, num=45)
view_angle = np.concatenate((view_angle, np.linspace(start=45, stop=0, num=45)), axis=0)
view_angle = np.concatenate((view_angle, np.linspace(start=0, stop=0, num=20)), axis=0)

# photo bleach correction based on first stack background and average
first_image_488 = io.imread(cell3_488[0])
first_mean488 = np.mean(first_image_488.reshape(-1))
first_max488 = np.max(first_image_488.reshape(-1))
bg488 = 20
first_image_560 = io.imread(cell3_560[0])
first_mean560 = np.mean(first_image_560.reshape(-1))
first_max560 = np.max(first_image_560.reshape(-1))
bg560 = 2

# loop through cell3
i = 0
for tiff_file_1, tiff_file_2 in zip(cell3_488, cell3_560):

    image_1 = io.imread(tiff_file_1)
    frame488_corrected = (first_mean488) / (np.mean(image_1.reshape(-1))) * (image_1)
    print(tiff_file_1)
    print((first_mean488) / (np.mean(image_1.reshape(-1))))

    image_2 = io.imread(tiff_file_2)
    frame560_corrected = (first_mean560 - bg560) / (np.mean(image_2.reshape(-1)) - bg560) * (image_2 - bg560)
    print(tiff_file_2)
    print((first_mean560 - bg560) / (np.mean(image_2.reshape(-1)) - bg560))

    layer1 = viewer.add_image(frame488_corrected, name='488', colormap=membrane_cmap, blending='translucent',
                              contrast_limits=[np.min(frame488_corrected), first_max488], opacity=1, gamma=0.5,
                              scale=(1.98, 1, 1))
    layer2 = viewer.add_image(frame560_corrected, name='560', colormap=nucleus_cmap, blending='additive',
                              contrast_limits=[np.min(frame560_corrected), first_max560], opacity=1, gamma=0.5,
                              scale=(1.98, 1, 1))
    viewer.dims.ndisplay = 3
    viewer.camera.center = (0, 500, 500)
    viewer.camera.angles = (0, view_angle[i], 90)
    viewer.camera.zoom = 0.5
    save_image = image_path + f'image_{i}.png'  # Change file extension if necessary-
    frame = viewer.screenshot(path=save_image, size=[1008, 1008])  # Take a screenshot of the current view
    writer.append_data(frame)  # Add the screenshot to the video
    viewer.layers.remove(layer1)
    viewer.layers.remove(layer2)
    i += 1

# readin data, cell3_cont
nchannels = [488, 560]
file_pattern = "Y:\Tian-Ming_Fu\Files_from_Janelia\LLS/20201209_LLS\LLCPK1_ER-mEmerald-H2B-mCherry\Cell3_Cont\GPUdecon/{}/*.tif"
channels = [file_pattern.format(i) for i in nchannels]
cell3_cont488 = glob.glob(channels[0])
cell3_cont488.sort()
cell3_cont560 = glob.glob(channels[1])
cell3_cont560.sort()
assert len(cell3_cont488) == len(cell3_cont560), "The number of TIFF files in each folder must be the same."

# cell3_cont viewing
zoom = np.linspace(start=0.5, stop=2.0, num=180)
zoom = np.concatenate((zoom, np.linspace(start=2.0, stop=1.0, num=200)), axis=0)
xcenter = np.linspace(start=500, stop=530, num=240)
xcenter = np.concatenate((xcenter, np.linspace(start=530, stop=530, num=200)), axis=0)
ycenter = np.linspace(start=500, stop=300, num=240)
ycenter = np.concatenate((ycenter, np.linspace(start=300, stop=300, num=200)), axis=0)
view_angle = np.linspace(start=0, stop=15, num=400)

# loop through cell3_cont
i = 0
for tiff_file_1, tiff_file_2 in zip(cell3_cont488, cell3_cont560):

    image_1 = io.imread(tiff_file_1)
    frame488_corrected = (first_mean488) / (np.mean(image_1.reshape(-1))) * (image_1)
    print(tiff_file_1)
    print((first_mean488) / (np.mean(image_1.reshape(-1))))

    image_2 = io.imread(tiff_file_2)
    frame560_corrected = (first_mean560 - bg560) / (np.mean(image_2.reshape(-1)) - bg560) * (image_2 - bg560)
    print(tiff_file_2)
    print((first_mean560 - bg560) / (np.mean(image_2.reshape(-1)) - bg560))

    layer1 = viewer.add_image(frame488_corrected, name='488', colormap=membrane_cmap, blending='translucent',
                              contrast_limits=[np.min(frame488_corrected), first_max488], opacity=1, gamma=0.5,
                              scale=(1.98, 1, 1))
    layer2 = viewer.add_image(frame560_corrected, name='560', colormap=nucleus_cmap, blending='additive',
                              contrast_limits=[np.min(frame560_corrected), first_max560], opacity=1, gamma=0.5,
                              scale=(1.98, 1, 1))

    viewer.dims.ndisplay = 3
    viewer.camera.angles = (0, view_angle[i], 90)
    viewer.camera.center = (0, ycenter[i], xcenter[i])
    viewer.camera.zoom = zoom[i]

    save_image = image_path + f'image_{i+100}.png'  # Change file extension if necessary-
    frame = viewer.screenshot(path=save_image, size=[1008, 1008])  # Take a screenshot of the current view
    writer.append_data(frame)  # Add the screenshot to the video
    viewer.layers.remove(layer1)
    viewer.layers.remove(layer2)
    i += 1

writer.close()