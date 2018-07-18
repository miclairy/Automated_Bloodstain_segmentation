# Standard imports
import cv2
import numpy as np
 
# Read image
img = cv2.imread("./images/cast off 162.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create()
 
# Detect blobs.
keypoints = detector.detect(gray)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imwrite("cast  off 162 blood dections.jpg", im_with_keypoints)
 
# Show keypoints
small = cv2.resize(im_with_keypoints, (0,0), fx=0.25, fy=0.25)
cv2.imshow("Keypoints", small)
cv2.waitKey(0)