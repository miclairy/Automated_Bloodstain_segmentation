import cv2
import numpy as np
import sys
import os
import time
from matplotlib import pyplot as plt
import bloodstain
import json

stains = []
#path = '/home/cosc/student/cba62/blood-spatter-analysis/Neural Net/bloodstains/Gwenda Cast Off/' 
path = "./images/"

def main():
    t0 = time.time()
    filename = path + sys.argv[1]
    print(filename)
    image = cv2.imread(filename)
    orginal = cv2.imread(filename)

    scale = float(sys.argv[2]) if len(sys.argv) >= 2 else 1
    
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # plt.hist(hsv_img.ravel(), 256, [0, 255])
    # plt.xlim([0, 360])
    # plt.show()
    blur = cv2.GaussianBlur(image, (3,3), 0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    gray_hsv = cv2.cvtColor(hsv_img, cv2.COLOR_BGR2GRAY)

    thresh = binarize_image(image, gray, gray_hsv, hsv_img)
    hist = cv2.calcHist( [gray_hsv], [0], None, [256], [0, 256] )
    remove_circle_markers(gray, thresh)

    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    
    cv2.drawContours(image, contours, -1, (0,0,255), 3)
    analyseContours(contours, orginal, image, scale)
   # label_stains()
    t1 = time.time()
    display_result(image)

    cv2.imwrite(sys.argv[1] + "_annotation.jpg", image)

def label_stains():

    labels = {"shapes" : [], "lineColor": [0, 255, 0, 128],
    "imagePath": sys.argv[1],
    "flags": {},
    "imageData" : None,
    "fillColor": [255, 0, 0,128]}
    i = 0
    for stain in stains:
        labels["shapes"].append(stain.label(" " + str(i)))
        i = i + 1

    mask_filename = path + os.path.splitext(sys.argv[1])[0] + '.json'
    with open(mask_filename, 'w') as outfile:
        json.dump(labels, outfile)


def analyseContours(contours, orginal, image, scale):
   # area = float('inf')
    count = 0
    for cnt in contours:
        
        stain = bloodstain.Stain(cnt, scale, orginal)
        stains.append(stain)
        stain.draw_ellipse(image)
        stain.annotate(image)
        if stain.ellipse:
          #  angle = stain.ellipse[2]
            count += 1 
            #  print("gamma ", angle)        

    #print("min area:", area)
    print("ellispe count: ", count)


def display_result(img_original) :
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


def binarize_image(img_original, gray, gray_hsv, hsv_img) :

    ret, thresh = cv2.threshold(gray_hsv, 0, 255, cv2.THRESH_OTSU)

    kernel = np.ones((3,3),np.uint8)
    erosion = cv2.erode(thresh, kernel, iterations = 2)
    dilation = cv2.dilate(thresh, kernel, iterations = 2)

    return thresh


if __name__ == '__main__':
    main()