import stain_segmentation
import sys
import os
from subprocess import call
import cv2

def label_images():
    # path = '/home/cosc/student/cba62/blood-spatter-analysis/Neural Net/test/downsampled/'
    # path = '/home/cosc/student/cba62/blood-spatter-analysis/image processing v1/images/'
    path = '/media/cba62/Elements/Cropped Data/' + sys.argv[1]

    for filename in os.listdir(path):
        if "jpg" in filename.lower() or "tif" in filename:
            call(["python3", "stain_segmentation.py", sys.argv[1] + filename, str(7)])
            # downsample(path, filename)
            
def downsample(path, filename):
    print(path + filename)
    image = cv2.imread(path + filename)
    rows, cols, _channels = map(int, image.shape)
    src = cv2.pyrDown(image, dstsize=(cols // 2, rows // 2))
    cv2.imwrite(path + filename, src)


label_images()