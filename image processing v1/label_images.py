import binary_image
import sys
import os
from subprocess import call

def label_images():
    path = '/home/cosc/student/cba62/blood-spatter-analysis/Neural Net/bloodstains/Maykee Expirated'

    for filename in os.listdir(path):
        if "jpg" in filename.lower() or "tif" in filename:
            call(["python3", "binary_image.py", filename, str(7)])


label_images()