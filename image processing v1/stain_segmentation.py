import cv2
import numpy as np
import sys
import os
import time
from matplotlib import pyplot as plt
import bloodstain
import json
import csv

stains = []
# path = '/home/cosc/student/cba62/blood-spatter-analysis/Neural Net/bloodstains/cast-off/' 
#path = "./images/"
path = '/media/cba62/Elements/Cropped Data/'
save_path = '/media/cba62/Elements/Result_data/'

def main():
   # t0 = time.time()
    filename = path + sys.argv[1]
    print(filename)
    image = cv2.imread(filename)
    orginal = cv2.imread(filename)
    scale = 7 if len(sys.argv) <= 2 else float(sys.argv[2])
    
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
    cv2.drawContours(image, contours, -1, (255,0,255), 3)
    analyseContours(contours, orginal, image, scale)
   # export_data()
    # label_stains()
    # t1 = time.time()
    display_result(thresh)

    cv2.imwrite(save_path + sys.argv[1], image)

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
    for stain in stains:
        labels["shapes"].append(stain.label(" " + str(i)))
        i = i + 1

    mask_filename = path + os.path.splitext(sys.argv[1])[0] + '.json'
    with open(mask_filename, 'w') as outfile:
        json.dump(labels, outfile)


def analyseContours(contours, orginal, image, scale):
   # area = float('inf')
    count = 0
    for contour in contours:
        
        stain = bloodstain.Stain(count, contour, scale, orginal)
        stains.append(stain)
        stain.draw_ellipse(image)
        stain.annotate(image)
        count += 1 

    print("Count: ", count)

def export_data():
    file_name = os.path.splitext(path + sys.argv[1])[0]
    with open(file_name + '_data.csv', 'w', newline='') as csvfile:
        data_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(["id", "position x", "position y", "area px", "area_mm", "width ellipse", "height ellipse", \
                        "angle", "gamma", "direction", "solidity", "circularity", "intensity"])
        for stain in stains:
            stain.write_data(data_writer)
        


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

def remove_rulers(image):
    edges = cv2.Canny(image, 90, 100)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=0, maxLineGap=0)
    y_top_count = {}
    y_bottom_count = {}    
    x_left_count = {}
    x_right_count = {}
    max_x_len = (None, 0)
    h, w = image.shape 
    
    for line in lines:
        x1,y1,x2,y2 = line[0]
        max_x_len = (line, max(max_x_len[1], abs(x1 - x2))) if abs(x1 - x2) > max_x_len[1] else max_x_len
        y_low = max(y1, y2)
        if y_low < h / 2:
            y_top_count = line_count(y_low, y_top_count)
        else:
            y_bottom_count = line_count(y_low, y_bottom_count)
        if x1 < w / 2:
            x_left_count = line_count(x1, x_left_count)
        else:
            x_right_count = line_count(x1, x_right_count)
        if x2 < w / 2:
            x_left_count = line_count(x2, x_left_count)
        else:
            x_right_count = line_count(x2, x_right_count)
        
    sort_top_y = sorted(y_top_count, key=y_top_count.get)
    y = max(sort_top_y[-20:]) + 125
    print(y)
    
    sort_left_x = sorted(x_left_count, key=x_left_count.get)
    x = sort_left_x[-1] + 40
    print(x)

    sort_right_x = sorted(x_right_count, key=x_right_count.get)
    w2 = min(sort_right_x[-4:]) - 2 * x 
    print(w2)

    sort_bottom_y = sorted(y_bottom_count, key=y_bottom_count.get)
    h2 = min(sort_bottom_y[-4:]) - y - 40# remove_bottom(image[y:y+h, x:x+w2], y)
    if h2 > 0:
        h = h2

    print(h)
    crop_img = image[y:y+h, x:x+w2]
   
    # display_result(crop_img)
    return x, y, w2, h

def remove_bottom(no_ruler_crop, y):
    max_x_len = (None, 0)
    edges = cv2.Canny(no_ruler_crop, 90, 100)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=0, maxLineGap=0)
    for line in lines:
        x1,y1,x2,y2 = line[0]
        max_x_len = (line, max(max_x_len[1], abs(x1 - x2))) if abs(x1 - x2) > max_x_len[1] else max_x_len
    x1,y1,x2,y2 = max_x_len[0][0]
    return max(y1, y2) - y

def line_count(x1, x_count):
    if x1 in x_count:
        x_count[x1] += 1
    else:
        x_count[x1] = 1
    return x_count



def binarize_image(img_original, gray, gray_hsv, hsv_img) :

    ret, thresh = cv2.threshold(gray_hsv, 0, 255, cv2.THRESH_TRIANGLE)
    # thresh = cv2.bitwise_not(thresh)

    kernel = np.ones((3,3),np.uint8)
    erosion = cv2.erode(thresh, kernel, iterations = 2)
    dilation = cv2.dilate(erosion, kernel, iterations = 2)

    return thresh


if __name__ == '__main__':
    main()