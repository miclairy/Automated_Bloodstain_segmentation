import cv2
import json
import numpy as np
import csv

class Stain:

    def __init__(self, id, contour, scale, original): # scale in px per mm
        self.contour = contour
        self.id = id
        moment = cv2.moments(contour)
        self.original = original
        self.position = (int(moment['m10'] / moment['m00']), int(moment['m01'] / moment['m00'])) if moment['m00'] > 0 else (10,10)
        self.area = cv2.contourArea(self.contour)
        self.area_mm = self.area * (1 / scale ** 2)
        self.ellipse, self.c = self.fit_ellipse()
        self.major_axis = None
        if self.ellipse is not None:
            (self.x_ellipse, self.y_ellipse), (self.width, self.height), self.angle = self.ellipse
            self.major_axis = self.calculate_major_axis()
        else:
            self.x_ellipse, self.y_ellipse, self.width, self.height, self.angle = [None] * 5
        
    def fit_ellipse(self):
        contour = self.contour
        offset = 0
        minus_offset = 0
        add_offset = 0
        if len(self.contour) >= 5 and self.area > 9:
            max_dist = 0
            extreme_i = 0
            for i in range(len(self.contour)):
                pt = self.contour[i][0]
                dist_center = ((self.position[0] - pt[0]) ** 2 + (self.position[1] - pt[1]) ** 2) ** 0.5
                if max_dist < dist_center:
                    max_dist = dist_center
                    extreme_i = i
                
            hull = cv2.convexHull(contour,returnPoints = False)
            concave_sections = cv2.convexityDefects(contour, hull)
            concave_pts = []
            if concave_sections is not None:
                for i in range(concave_sections.shape[0]-1):
                    s, e, f, d = concave_sections[i,0]
                    concave_pts.append(tuple(self.contour[f][0]))

            end_tail = None
            start_tail = None
            i = extreme_i
            k = extreme_i
            _, _ , max_width, height = cv2.boundingRect(self.contour)
            small_width = True

            while i < len(self.contour) and k > 0 and small_width:
                pt_1 = self.contour[i][0]
                pt_2 = self.contour[k][0]
                dist = ((pt_1[0] - pt_2[0]) ** 2 + (pt_1[1] - pt_2[1]) ** 2) ** 0.5
                if (dist / max_width) > 0.3:
                    small_width = False
                    end_tail = i
                    start_tail = k
                i += 1
                k -= 1
            

            # for i in range(extreme_i, len(self.contour)):
            #     pt = self.contour[i][0]
            #     if tuple(pt) in concave_pts:
            #         end_tail = i
            #         break
            
            # i = 0
            # for i in range(extreme_i, 0, -1):
            #     pt = self.contour[i][0]
            #     if tuple(pt) in concave_pts:
            #         start_tail = i
            #         break

            if end_tail and start_tail:
                contour = np.concatenate((self.contour[:start_tail], self.contour[end_tail:]))
            if len(contour) > 5:
                # contour = self.contour
                 
                return cv2.fitEllipse(np.array(contour)), contour
        return None, None
        
    def draw_ellipse(self, image):

        if self.ellipse is not None:
            cv2.ellipse(image, self.ellipse, (0,255,0), 1)

    def circularity(self):
        if self.ellipse:
            return self.width / self.height
        else:
            return float('inf')

    def orientaton(self):
        if self.ellipse:
            if self.direction()[0] == "left":
                gamma = (self.angle + 180) % 360
            else:
                gamma = self.angle
            return [self.angle, gamma]
        return [float('inf'), float('inf')]


    def direction(self):
        if self.ellipse:
            x = self.x_ellipse
            angle = self.angle
            left_half = []
            right_half = []
            
            for pt in self.contour:
                pt = pt[0]
                side = (pt[0] - x)
                if side > 1:
                    right_half.append(pt)
                else:
                    left_half.append(pt)
            left_half = np.array(left_half)
            
            right_half = np.array(right_half)

        else:
            left_half = self.contour[ : len(self.contour) // 2]
            right_half = self.contour[len(self.contour) // 2 : ]
            angle = float('inf')
        
        if np.abs(self.area_half(left_half) - self.area_half(right_half)) <= 0.005:  
            direction = "?"
        elif self.area_half(left_half) < self.area_half(right_half):
            if angle < 90:
                direction = ("left", "down")
            else:
                direction = ("left", "up")
        else:
            if angle < 90:
                direction = ("right", "up")
            else:
                direction = ("right", "down")

        return direction

    def calculate_major_axis(self):
        x = self.position[0] 
        y = self.position[1]
        direction = self.direction()

        if self.angle:
            pty = np.cos(np.deg2rad(self.angle)) * 1000000
            ptx = np.sin(np.deg2rad(self.angle)) * 1000000
            x0 = int(x + ptx)
            x1 = int(x - ptx)
            y0 = int(y - pty)
            y1 = int(y + pty)
            
            if direction != "?":
                if direction[0] == "left":
                    x_use = max(x0, x1)
                else:
                    x_use = min(x0, x1)
                if direction[1] == "up":
                    y_use = max(y0, y1)
                else:
                    y_use = min(y0, y1)
                # print(x, y)
                return sorted([(x, y), (int(x_use), int(y_use))], key=lambda x : x[0]) 
            return sorted([(int(x0), int(y0)), (int(x1), int(y1))], key=lambda x : x[0]) 

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
    
    def annotate(self, image, annotations={
        'ellipse':True, 'id':False, 'directionality':False, 
        'center':False, 'gamma':False, 'direction_line': False}):
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = ""
        if len(self.c) > 0:
           cv2.drawContours(image, [self.c], 0, (255,255,0), 1)
        #    cv2.drawContours(image, [self.right_half], 0, (255,255,0), 3)

        if annotations['ellipse'] and self.ellipse:
            self.draw_ellipse(image)
        if annotations['id']:
            text += str(self.id)
        if annotations['directionality']:
            text += " " + str(self.direction())
        if annotations['center']:
            cv2.circle(image, (self.position[0], self.position[1]), 2, (255, 255, 255), -1)   
        if annotations['gamma']:
            text += " " + str(self.orientaton()[1])
        if annotations['direction_line'] and self.angle:
            cv2.line(image , self.major_axis[0], self.major_axis[1], (255,0,0), 2)
        cv2.putText(image, text, (int(self.position[0] + 10), int(self.position[1] + 30)), font, 1, (0,255,255), 2, cv2.LINE_AA)

    def label(self):
        points = [x[0] for x in self.contour.tolist() ]

        return [self.id] + points

    def obj_format(self, width, height):
        points = [x[0] for x in self.contour.tolist() ]
        str_points = ""
        for pt in points:
            str_points += "{} {} 0\n".format(pt[0] / width, pt[1] / height)
        return str_points

    def get_summary_data(self):
        summary_data = [self.id, self.position[0], self.position[1], int(self.area), self.area_mm, self.width, self.height, \
                self.orientaton()[0], self.orientaton()[1], str(self.direction()), self.solidity(), self.circularity(), self.intensity(self.original)]
        formatted = []
        for data in summary_data:
            if (data == float('inf')):
                data = None
            if (isinstance(data, float)):
                formatted.append("{:.3f}".format(data))
            else:
                formatted.append(data)
        return formatted
    
    def write_data(self, writer):
        writer.writerow(self.get_summary_data())

    
