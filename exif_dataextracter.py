#!/usr/bin/env python3

# Disclaimer: This script is for educational purposes only.
# Do not use against any photos that you don't own or have authorization to test.

import os
import csv
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS


def convert_decimal_degrees(degree, minutes, seconds, direction):
    decimal_degrees = degree + minutes / 60 + seconds / 3600
    if direction in ["S", "W"]:
        decimal_degrees *= -1
    return decimal_degrees


def create_google_maps_url(gps_coords):
    dec_deg_lat = convert_decimal_degrees(
        float(gps_coords["lat"][0]),
        float(gps_coords["lat"][1]),
        float(gps_coords["lat"][2]),
        gps_coords["lat_ref"]
    )
    dec_deg_lon = convert_decimal_degrees(
        float(gps_coords["lon"][0]),
        float(gps_coords["lon"][1]),
        float(gps_coords["lon"][2]),
        gps_coords["lon_ref"]
    )
    return f"https://maps.google.com/?q={dec_deg_lat},{dec_deg_lon}"


# Prepare directories
cwd = os.getcwd()
image_dir = os.path.join(cwd, "images")
os.chdir(image_dir)
files = os.listdir()

if len(files) == 0:
    print("You don't have any files in the ./images folder.")
    exit()

# Write to CSV
with open("../exif_data.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Filename", "Tag", "Value"])

    for file in files:
        try:
            image = Image.open(file)
            gps_coords = {}
            writer.writerow([file, "== Begin EXIF Data ==", ""])

            exif_data = image._getexif()
            if exif_data is None:
                writer.writerow([file, "No EXIF data found", ""])
                continue

            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag)
                if tag_name == "GPSInfo":
                    for key, val in value.items():
                        gps_tag = GPSTAGS.get(key)
                        writer.writerow([file, gps_tag, val])
                        if gps_tag == "GPSLatitude":
                            gps_coords["lat"] = val
                        elif gps_tag == "GPSLongitude":
                            gps_coords["lon"] = val
                        elif gps_tag == "GPSLatitudeRef":
                            gps_coords["lat_ref"] = val
                        elif gps_tag == "GPSLongitudeRef":
                            gps_coords["lon_ref"] = val
                else:
                    writer.writerow([file, tag_name, value])

            if gps_coords:
                maps_url = create_google_maps_url(gps_coords)
                writer.writerow([file, "Google Maps Link", maps_url])

            writer.writerow([file, "== End EXIF Data ==", ""])

        except IOError:
            print(f"File format not supported or unreadable: {file}")

os.chdir(cwd)
