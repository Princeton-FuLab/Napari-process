import glob
import os
from skimage import io
import numpy as np
import json

file_dir = "Y:\Andy Zhang\Data/20240402_Compact_PEARLS_V2_on_MOSAIC\Duty_cycle_photobleaching\Square\PEARLS/Old_batch_collagen"
folders = [f.path for f in os.scandir(file_dir) if f.is_dir()]
number_of_stacks = 6

for one_folder in folders:
    one_set = glob.glob(one_folder + '/*.tif')
    one_set.sort()
    one_file_peak = []
    one_file_mean = []
    image_1 = []
    for one_file in one_set[:number_of_stacks]:
        # read in single file
        print(one_file)
        image_1 = io.imread(one_file)

        # calculate mean/peak
        one_file_peak = np.concatenate((one_file_peak, np.max(image_1, axis=(1, 2))), axis=0)
        one_file_mean = np.concatenate((one_file_mean, np.mean(image_1, axis=(1, 2))), axis=0)

    # simply create a dictionary
    data = {'peak Intensity': one_file_peak.tolist(),'mean Intensity': one_file_mean.tolist()}

    # save analysis in each folder
    saving_file = one_folder + '/peak_mean_analysis.json'
    with open(saving_file, 'w') as file:
        json.dump(data, file, indent=4)



