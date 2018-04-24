import cv2
import numpy as np

img_original = cv2.imread('./images/Panorama 64 cropped.tif')
# img_original = cv2.imread('./images/211 Rep 4 MAX.JPG')

height,width = img_original.shape[:2]

lower_hue = 25.0 / 360
upper_hue = 325.0 / 360
saturation = 0.2
value = 0.1

lower_threshold = np.array([lower_hue * 179, saturation * 255, value * 255])
upper_threshold = np.array([upper_hue * 179, 255, 255])

hsv_img = cv2.cvtColor(img_original, cv2.COLOR_BGR2HSV)

col_thresh = cv2.inRange(hsv_img, lower_threshold, upper_threshold)

kernel = np.ones((3,3),np.uint8)
erosion = cv2.erode(col_thresh,kernel,iterations = 2)
dilation = cv2.dilate(erosion, kernel, iterations = 2)
ret, labels = cv2.connectedComponents(dilation)

# make pretty colours
label_hue = np.uint8(179 * labels / np.max(labels))
blank_ch = 255 * np.ones_like(label_hue)
labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

labeled_img[label_hue==0] = 0

blur = cv2.GaussianBlur(img_original, (9,9), 0)
# Convert the image to grayscale for processing
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
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
   

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=100,
                            param2=58, minRadius=24, maxRadius=82)

    img = labeled_img.copy()
    if circles is not None:
        circles = np.uint16(np.around(circles))

        for i in circles[0,:]:
            # Draw the outer circle
            cv2.circle(img,(i[0],i[1]),i[2] + 2,(0,0,0),-2)
            # Draw the center of the circle
          #  cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
            
    small = cv2.resize(dilation, (0,0), fx=0.125, fy=0.125)
    cv2.imshow('Blood Spatter', small)

    if cv2.waitKey(100) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
