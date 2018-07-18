import cv2
import json
import numpy as np
import csv

class Stain:

    def __init__(self, id, contour, scale, original): # scale in px per mm
        self.contour = contour
        # print(contour)
        self.id = id
        moment = cv2.moments(contour)
        self.original = original
        self.position = (int(moment['m10'] / moment['m00']), int(moment['m01'] / moment['m00'])) if moment['m00'] > 0 else (10,10)
        self.ellipse = cv2.fitEllipse(self.contour) if len(self.contour) >= 5 else None
        self.area = cv2.contourArea(self.contour)
        self.area_mm = self.area * (1 / scale ** 2)
        if self.ellipse is not None:
            (self.x_ellipse, self.y_ellipse), (self.width, self.height), self.angle = self.ellipse
        else:
            self.x_ellipse, self.y_ellipse, self.width, self.height, self.angle = [None] * 5
        
    def draw_ellipse(self, image):

        if self.ellipse is not None:
           cv2.ellipse(image, self.ellipse, (0,255,0), 2)

    def circularity(self):
        if self.ellipse:
            return self.width / self.height
        else:
            return float('inf')

    def orientaton(self):
        if self.ellipse:
            
            minor = self.width / 2
            major = self.height / 2
            if self.direction() == "left":
                gamma = (self.angle + 180) % 360
            else:
                gamma = self.angle
            return [self.angle, gamma]
        return [float('inf'), float('inf')]


    def direction(self):
        if self.ellipse:
            x = self.x_ellipse
            y = self.y_ellipse
            angle = self.angle
            ptx = np.cos(np.deg2rad(angle)) * self.width / 2
            pty = np.sin(np.deg2rad(angle)) * self.width / 2
            x0 = int(x + ptx)
            x1 = int(x - ptx)
            y0 = int(y - pty)
            y1 = int(y + pty)
            left_half = []
            right_half = []
            
            for pt in self.contour:
                pt = pt[0]
                side = (x1 - x0) * (pt[1] - y0) - (pt[0] - x0) * (y1 - y0)
                if side > 1:
                    left_half.append(pt)
                else:
                    right_half.append(pt)
            left_half = np.array(left_half)
            
            right_half = np.array(right_half)

        else:
            left_half = self.contour[ : len(self.contour) // 2]
            right_half = self.contour[len(self.contour) // 2 : ]
            angle = float('inf')

        if angle < 90:
            direction = "up "
        else:
            direction = "down "
        
        if np.abs(self.area_half(left_half) - self.area_half(right_half)) <= 0.005:  
            direction += "?"
        elif self.area_half(left_half) < self.area_half(right_half):
            direction += "left"
        else:
            direction += "right"
        # print(self.area_half(left_half), self.area_half(right_half), direction)
        return direction

    def area_half(self, half_contour):
        if len(half_contour) > 0:
            hull_half = cv2.contourArea(cv2.convexHull(half_contour))
            if hull_half > 0:
                return cv2.contourArea(half_contour) / hull_half
        return -1


    def intensity(self, image):
        grey = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
        mask = np.zeros(grey.shape, np.uint8)
        cv2.drawContours(mask, [self.contour], 0, 255, -1)
        intensity = cv2.mean(grey, mask=mask)
        return intensity[0] / 255

    def solidity(self):
        '''regularity of element margin'''
        hull = cv2.convexHull(self.contour)
        hull_area = cv2.contourArea(hull)
        if hull_area > 0:
            return self.area / hull_area
        else:
            return None
    
    def annotate(self, image):
        font = cv2.FONT_HERSHEY_SIMPLEX
        anotation = str(self.id) #"({} {:.2f})".format(self.direction(), self.orientaton()[0])
        cv2.circle(image, (self.position[0], self.position[1]), 2, (255, 255, 255), -1)     
        #
        #if len(self.left_half) > 0:
        #    cv2.drawContours(image, [self.left_half], 0, (255,255,0), 3)
        cv2.putText(image, anotation, (int(self.position[0] + 10), int(self.position[1] + 30)), font, 1, (0,255,255), 2, cv2.LINE_AA)

    def label(self, id):
        points = [x[0] for x in self.contour.tolist() ]
        label = {"points": points, "fill_color": None, "line_color": None, "label": "bloodstain" + id}
        # print(json.dumps(label, indent=4))
        return label
    
    def write_data(self, writer):
        writer.writerow([self.id, self.position[0], self.position[1], self.area, self.area_mm, self.width, self.height, \
                        self.orientaton()[0], self.orientaton()[1], self.direction(), self.solidity(), self.circularity(), self.intensity(self.original)])

    
