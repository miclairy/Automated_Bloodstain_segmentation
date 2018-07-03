import cv2
import json
import numpy as np

class Stain:

    def __init__(self, contour, scale, original):
        self.contour = contour
        # print(contour)
        moment = cv2.moments(contour)
        self.original = original
        self.position = (1,1) #(int(moment['m10'] / moment['m00']), int(moment['m01'] / moment['m00']))
        self.ellipse = cv2.fitEllipse(self.contour) if len(self.contour) >= 5 else None
        self.area = cv2.contourArea(self.contour)
        self.area_mm = self.area * (scale ** 2)
        self.directionality = float('inf')     

    def draw_ellipse(self, image):

        if self.ellipse is not None:
            cv2.ellipse(image, self.ellipse, (0,255,0), 2)

    def circularity(self):
        if self.ellipse:
            (x, y), (width, height), angle = self.ellipse
            return width / height
        else:
            return float('inf')

    def orientaton(self):
        if self.ellipse:
            (x, y), (width, height), angle = self.ellipse
            minor = width / 2
            major = height / 2
            if angle <= 180:
                gamma = angle
            else:
                gamma = (angle + 180) % 360
            return [angle, gamma]
        return [float('inf'), float('inf')]

    def intensity(self, image):
        grey = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
        mask = np.zeros(grey.shape, np.uint8)
        cv2.drawContours(mask, [self.contour], 0, 255, -1)
        intensity = cv2.mean(self.original, mask=mask)
        return intensity

    def solidity(self):
        '''regularity of element margin'''
        hull = cv2.convexHull(self.contour)
        hull_area = cv2.contourArea(hull)
        return self.area / hull_area
    
    def annotate(self, image):
        font = cv2.FONT_HERSHEY_SIMPLEX
        anotation = "(angle:{:.2f}, gamma:{:.2f})".format(self.orientaton()[0], self.orientaton()[1])
        cv2.circle(image, (self.position[0], self.position[1]), 2, (255, 255, 255), -1)
        cv2.putText(image, anotation, (int(self.position[0] + 10), int(self.position[1] + 30)), font, 1, (0,255,255), 2, cv2.LINE_AA)

    def label(self, id):
        points = [x[0] for x in self.contour.tolist() ]
        label = {"points": points, "fill_color": None, "line_color": None, "label": "bloodstain" + id}
        # print(json.dumps(label, indent=4))
        return label
    
    
