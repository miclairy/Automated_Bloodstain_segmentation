import cv2
import numpy as np

def nothing(x):
    # We need a callback for the createTrackbar function.
    # It doesn't need to do anything, however.
    pass

img_original = cv2.imread('/home/cosc/student/cba62/Documents/stain segmentation matlab code/images/cast_off_5.tif')
height,width = img_original.shape[:2]

lower_hue = 0.0 / 360
upper_hue = 360.0 / 360
saturation = 0.2
value = 0.1

lower_threshold = np.array([lower_hue * 179, saturation * 255, value * 255])
upper_threshold = np.array([upper_hue * 179, 255, 255])

hsv_img = cv2.cvtColor(img_original, cv2.COLOR_BGR2HSV)

col_thresh = cv2.inRange(hsv_img, lower_threshold, upper_threshold)

kernel = np.ones((3,3),np.uint8)
erosion = cv2.erode(col_thresh,kernel,iterations = 2)
dilation = cv2.dilate(erosion, kernel, iterations = 2)
ret, labels = cv2.connectedComponents(col_thresh)


label_hue = np.uint8(179 * labels / np.max(labels))
blank_ch = 2555 * np.ones_like(label_hue)
print(len(label_hue), len(blank_ch))
# labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

# labeled_img = cv2.cvtColor(label_hue, cv2.COLOR_HSV2BGR)

# labeled_img[label_hue==0] = 0

# Convert the image to grayscale for processing
# gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
#
# edges = cv2.Canny(gray, 600, 600)
#
# gray_blur = cv2.medianBlur(gray, 51)
#
# ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
# diff = cv2.subtract(thresh, gray)

while True:

    # small = cv2.pyrDown(gray, dstsize=(width // 2, height // 2))
   # cv2.imshow('Blood Spatter', small)
    small = cv2.resize(label_hue, (0,0), fx=0.125, fy=0.125)

    cv2.imshow('Blood Spatter', small)

    if cv2.waitKey(100) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
