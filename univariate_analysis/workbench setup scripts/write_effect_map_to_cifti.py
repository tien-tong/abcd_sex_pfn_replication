import nibabel as nib
import pandas as pd
import sys
import os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from pfn_config import cfg  # file paths come from CONFIG.txt at the repo root

if __name__ == "__main__":
    # Get the filename of the data to be converted and the filename to be saved to
    input_filename = sys.argv[1]
    save_filename = sys.argv[2]

    # Read in input_filename
    data_to_be_converted = pd.read_csv(input_filename)
    print(f"Value from file to be converted: {data_to_be_converted['0'].values[0]}")

    # Use working cifti header to create image with new data
    working_cifti_file = nib.load(cfg["CIFTI_TEMPLATE_DSCALAR"])
    cifti_header = working_cifti_file.header

    # Create and save new cifti image with the inputted data
    new_cifti_img = nib.Cifti2Image(np.asanyarray(data_to_be_converted.T), header=cifti_header)
    print(f"Value in new cifti image before saving: {new_cifti_img.get_fdata()[0][0]}")
    nib.loadsave.save(new_cifti_img, save_filename)

    #print(f"Converted file saved to {save_filename}!")

    # Save command run into commands_run file
    command_run = f"python3 write_effect_map_to_cifti.py '{input_filename}' '{save_filename}'\n" 
    f = open(cfg["COMMANDS_LOG"], "a+")
    f.write(command_run)
    f.close()


    reloaded_img = nib.load(save_filename)
    print(f"Value from converted image reloaded: {reloaded_img.get_fdata()[0][0]}")

