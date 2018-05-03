import cv2
import numpy as np
from matplotlib import pyplot as plt


# img_original = cv2.imread('./images/Panorama 64 cropped.tif')
# img_original = cv2.imread('./images/211 Rep 4 MAX.JPG')
img_original = cv2.imread('./images/cast off 162.jpg')
# img_original = cv2.imread('./images/Exp. 51.jpg')
# img_original = cv2.imread('./images/Impact 1.jpg')
# img_original = cv2.imread('/home/cosc/student/cba62/Documents/COSC428/lab02/images/windows.jpg')

height,width = img_original.shape[:2]


# lower_hue = 25.0 / 360
# upper_hue = 325.0 / 360
lower_hue = 0.0 / 360
upper_hue = 360.0 / 360
saturation = 0.2
value = 0.1

lower_threshold = np.array([lower_hue * 179, saturation * 255, value * 255])
upper_threshold = np.array([upper_hue * 179, 255, 255])

hsv_img = cv2.cvtColor(img_original, cv2.COLOR_BGR2HSV)

col_thresh = cv2.inRange(hsv_img, lower_threshold, upper_threshold)

blur = cv2.GaussianBlur(img_original, (9,9), 0)
# hsv_img = cv2.GaussianBlur(hsv_img, (9,9), 0)

# Convert the image to grayscale for processing
gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
gray_hsv = cv2.cvtColor(hsv_img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray_hsv, 0, 255, cv2.THRESH_TRIANGLE )
print("thres value: ", ret)
# edges = cv2.Canny(gray, 66, 100)

kernel = np.ones((3,3),np.uint8)
erosion = cv2.erode(thresh ,kernel,iterations = 2)
dilation = thresh# cv2.dilate(thresh, kernel, iterations = 2)

ret, labels = cv2.connectedComponents(dilation)

# make pretty colours
label_hue = np.uint8(179 * labels / np.max(labels))
blank_ch = 255 * np.ones_like(label_hue)
labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

labeled_img[label_hue==0] = 0
   
hist = cv2.calcHist( [gray_hsv], [0], None, [256], [0, 256] )


circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=100,
                        param2=58, minRadius=24, maxRadius=82)

if circles is not None:
    circles = np.uint16(np.around(circles))

    for i in circles[0,:]:
        # Draw the outer circle
        cv2.circle(dilation, (i[0],i[1]),i[2] + 10, (0,255,0), -2)
        # Draw the center of the circle
        #  cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

im2, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img_original, contours, -1, (0,0,255), 3)

font = cv2.FONT_HERSHEY_SIMPLEX

area = 0
for cnt in contours:
    area += cv2.contourArea(cnt)
    if len(cnt) >= 5:
        ellipse = cv2.fitEllipse(cnt)
        (x, y) = ellipse[0]
        (MA, ma) = ellipse[1]
        angle = ellipse[2]
        # cv2.ellipse(img_original, ellipse, (0,255,0), 2)
      #  print("gamma ", angle)
        # cv2.putText(img_original, str(angle), (int(x), int(y)), font, 1, (0,0,0), 2, cv2.LINE_AA)
# print("mean area:", area / len(contours))

while True:

    # plt.hist(hsv_img.ravel(), 256, [0, 255])
    # plt.xlim([0, 360]
    # plt.show()
    small = cv2.resize(img_original, (0,0), fx=0.25, fy=0.25)
    # cv2.imwrite("exp 1 hsv.jpg", hsv_img)
    cv2.imshow('Blood Spatter', small)
    
    if cv2.waitKey(100) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break