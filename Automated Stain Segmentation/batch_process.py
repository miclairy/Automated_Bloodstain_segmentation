import stain_segmentation
import sys
import os
from subprocess import call
import cv2
from parse_arguements import parse_batch_args
import progressbar

def get_folder(): 
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
    
    return path
    
def segment_images(path, out_path, scale, progressBar=None):
    percent = 0
    increment = (1 / len(os.listdir(path))) * 100
    for filename in progressbar.progressbar(os.listdir(path)):
        out_name = filename + "-result.jpg"    
        if out_name not in os.listdir(out_path):
            if "jpg" in filename.lower() or "tif" in filename:
                f = path.strip() + filename.strip()
                # change to python on if errors
                call(["python3", "stain_segmentation.py", "-F", f , "-s", str(scale), "-o", out_path + filename.strip(), "-b", "True"]) 
                # args = {'filename': None, 'full_path': f, 'batch': True, 'scale': scale, 'output_path': out_path + filename.strip()}
                # stain_segmentation.CLI(args)
                # downsample(path, filename)
                if progressBar:
                    percent += increment
                    progressBar.setValue(percent)
    if progressBar:
        progressBar.hide()
            
def downsample(path, filename):
    print(path + filename)
    image = cv2.imread(path + filename)
    rows, cols, _channels = map(int, image.shape)
    src = cv2.pyrDown(image, dstsize=(cols // 2, rows // 2))
    cv2.imwrite(path + filename, src)

def crop(path, out_path):
    for filename in progressbar.progressbar(os.listdir(path)):
        if "jpg" in filename.lower() or "tif" in filename:
            f = path.strip() + filename.strip()
        call(["python3", "crop.py", "-F", f , "-o", out_path + filename.strip(), "-b", "True"]) 


if __name__ == '__main__':
    path = get_folder()
    out_path = path if not parse_batch_args()['output_path'] else parse_batch_args()['output_path']
    scale = 7 if not parse_batch_args()['scale'] else parse_batch_args()['scale']
    if path != None:
        segment_images(path, out_path, scale)
        # crop(path, out_path)