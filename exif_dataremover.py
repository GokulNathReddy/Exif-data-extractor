#!/usr/bin/env python3

# Disclaimer: This script is for educational purposes only.
# Do not use against any photos that you don't own or have authorization to test.

# This script removes EXIF data from .JPG and .TIFF files in the ./images folder.

import os
from PIL import Image

# Set up working directory and image folder path
cwd = os.getcwd()
image_dir = os.path.join(cwd, "images")
os.chdir(image_dir)

# Get list of files in the image folder
files = os.listdir()

# Check if any files exist
if len(files) == 0:
    print("You don't have any files in the ./images folder.")
    exit()

# Process each file and remove EXIF data
for file in files:
    try:
        img = Image.open(file)
        img_data = list(img.getdata())

        img_no_exif = Image.new(img.mode, img.size)
        img_no_exif.putdata(img_data)
        img_no_exif.save(file)

    except IOError:
        print(f"File format not supported or unreadable: {file}")
