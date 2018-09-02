import stain_segmentation
import sys
import os
from subprocess import call
import cv2
from parse_arguements import parse_batch_args

def segment_images():
    
    # path = '/home/cosc/student/cba62/blood-spatter-analysis/Neural Net/test/downsampled/'
    # path = '/home/cosc/student/cba62/blood-spatter-analysis/image processing v1/images/'
    path = '/media/cba62/Elements/Cropped Data/'
    
    path = None if not parse_batch_args()['folder'] else path + parse_batch_args()['folder']
    full_path = parse_batch_args()['full_path']
    if full_path:
        path = full_path
    if not path:
        print("No folder selected")
        return 
    print(path)
    

    for filename in os.listdir(path):
        if "jpg" in filename.lower() or "tif" in filename:
            print(filename)
            call(["python3", "stain_segmentation.py", "-F", path.strip() + filename.strip() , "-s " + str(7), "-b", "True"])
            # downsample(path, filename)
            
def downsample(path, filename):
    print(path + filename)
    image = cv2.imread(path + filename)
    rows, cols, _channels = map(int, image.shape)
    src = cv2.pyrDown(image, dstsize=(cols // 2, rows // 2))
    cv2.imwrite(path + filename, src)


if __name__ == '__main__':
    segment_images()