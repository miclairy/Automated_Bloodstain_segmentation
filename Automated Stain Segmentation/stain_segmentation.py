import cv2
import numpy as np
import sys
import os
import time
from matplotlib import pyplot as plt
import bloodstain
import json
import csv
from parse_arguements import parse_args
from pattern import Pattern
import progressbar

# path = '/home/cosc/student/cba62/blood-spatter-analysis/Neural Net/bloodstains/cast-off/' 
#path = "./images/"
path = '/media/cba62/Elements/Cropped Data/'
save_path = '/media/cba62/Elements/Result_data/'
pattern = Pattern()

def CLI(args={}):
    args = parse_args() if not args else args
    print(args)
    filename = None if not args['filename'] else path + args['filename']
    full_path = args['full_path']
    if full_path:
        filename = full_path

    if not filename:
        print("No file selected")
        return 
    print("\nProcessing: " + filename)
    
    save_path = set_save_path(filename, args['output_path'])
    pattern.scale = args['scale']
    if pattern.scale < 1:
        print("Warning scale is less than 1")
    
    image = cv2.imread(filename)
    orginal = cv2.imread(filename)

    if image is None:
        print("No image file found")
        return

    batch = args['batch']

    height, width = image.shape[:2]
    pattern.image = image
    pattern.name = filename
    print("Segmenting stains")
    result = stain_segmentation(image, orginal)
    cv2.drawContours(image, pattern.contours, -1, (255,0,255), 1)
    for stain in pattern.stains:
            stain.annotate(image)
    if not batch:
        result_preview(result)
    cv2.imwrite(save_path + '-result.jpg', result)
    print("Analysing Stains")
    export_stain_data(save_path)
    export_obj(save_path, width, height)
    print("\nCalculating Pattern Metrics")
    to_calculate= {'linearity': True, 
                 'convergence': False, 'distribution': True}
    pattern.export(save_path, to_calculate, batch)
    print("\nResults found in files beginning: " + save_path)
    print("Done :)")


def set_save_path(full_path, output_path):
    if output_path:
        return output_path 
    
    if full_path:
        save_path = os.path.splitext(full_path)[0]
    else:
        save_path =  '/media/cba62/Elements/Result_data/' + args['filename']
    save_path = os.path.splitext(save_path)[0]
    return save_path

def stain_segmentation(image, orginal):

    pattern.clear_data()
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    blur = cv2.GaussianBlur(image, (3,3), 0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    gray_hsv = cv2.cvtColor(hsv_img, cv2.COLOR_BGR2GRAY)
    
    thresh = binarize_image(image, gray)
    thresh = cv2.bitwise_not(thresh)

    hist = cv2.calcHist( [gray_hsv], [0], None, [256], [0, 256] )
    remove_circle_markers(gray, thresh)
    kernel = np.ones((3,3),np.uint8)
    cv2.imwrite('./flipped' + '-binary.jpg', thresh)

    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)     
    analyseContours(contours, hierarchy, orginal, image, pattern.scale)
    
    return image

def crop_image(image):
    x, y, w, h = remove_rulers(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    return image[y:y+h, x:x+w]

def label_stains():

    labels = {"shapes" : [], "lineColor": [0, 255, 0, 128],
    "imagePath": sys.argv[1],
    "flags": {},
    "imageData" : None,
    "fillColor": [255, 0, 0,128]}
    i = 0
    for stain in pattern.stains:
        labels["shapes"].append(stain.label(" " + str(i)))
        i = i + 1

    mask_filename = path + os.path.splitext(sys.argv[1])[0] + '.json'
    with open(mask_filename, 'w') as outfile:
        json.dump(stain.label())

def analyseContours(contours, hierarchy, orginal, image, scale):
   # area = float('inf')
    count = 0
    outer_contours = []
    for i in range(len(contours)):
        contour = contours[i]
        if hierarchy[0,i,3] == -1:
            outer_contours.append(contour)
            if cv2.contourArea(contour) > 1:
                stain = bloodstain.Stain(count, contour, scale, orginal)
                pattern.add_stain(stain)
                count += 1
    pattern.contours = outer_contours  
    print("Found {} stains".format(count))

def export_stain_data(save_path, progressBar=False):
    
    with open(save_path + '_data.csv', 'w', newline='') as csvfile:
        data_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(["id", "position x", "position y", "area px", "area_mm", "width ellipse", "height ellipse", \
                        "angle", "gamma", "direction", "solidity", "circularity", "intensity"])
        with open(save_path + "_stains.csv", 'w') as point_file:
            points_writer = csv.writer(point_file, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            i = 0
            for stain in progressbar.progressbar(pattern.stains):
                stain.write_data(data_writer)
                points_writer.writerow(stain.label())
                if (progressBar):
                    i += (1 / len(pattern.stains)) * 50
                    progressBar.setValue(i)


def export_obj(save_path, width, height):
    # save_path = "E:\\PointNet_Data\\" + save_path.split("Cropped Data\\")[1]
    file_name = os.path.splitext(save_path)[0]
    print(file_name)
    with open(file_name + '_points.pts', 'w', newline='') as f:
        for stain in pattern.stains:
            f.write(stain.obj_format(width, height) )

def result_preview(img_original) :
    print("Press 'q' to close preview")
    while True:
        # plt.hist(hsv_img.ravel(), 256, [0, 255])
        # plt.xlim([0, 360])
        # plt.show()
        small = cv2.resize(img_original, (0,0), fx=0.25, fy=0.25)
        cv2.imshow('Blood Spatter', small)

        if cv2.waitKey(100) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

def remove_circle_markers(gray, img):
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=100,
                                param2=58, minRadius=24, maxRadius=82)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            cv2.circle(img, (i[0],i[1]),i[2] + 10, (0,0,0), -2)


def binarize_image(img_original, gray) :

    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 99, 10)
    # thresh = cv2.bitwise_not(thresh)
    
    kernel = np.ones((3,3),np.uint8)
    erosion = cv2.erode(thresh, kernel, iterations = 2)
    dilation = cv2.dilate(erosion, kernel, iterations = 2)

    return dilation


if __name__ == '__main__':
    CLI()