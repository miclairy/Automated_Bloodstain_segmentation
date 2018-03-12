# hough_circle.py

import cv2
import numpy as np

def nothing(x):
    # We need a callback for the createTrackbar function.
    # It doesn't need to do anything, however.
    pass

img_original = cv2.imread('./images/Panorama 73 cropped.tif')
height,width = img_original.shape[:2]

# Convert the image to grayscale for processing
gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)


while True:
    gray_blur = cv2.medianBlur(gray, 5)
    # thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 1)
    # small = cv2.resize(gray_blur, (0,0), fx=0.5, fy=0.5)
    small = cv2.pyrDown(img_original, dstsize=(width // 4, height // 4))
    cv2.imshow('Blood Spatter', small)

    if cv2.waitKey(100) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
