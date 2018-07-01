import cv2
import json

class Stain:

    def __init__(self, contour, scale):
        self.contour = contour
        # print(contour)
        moment = cv2.moments(contour)
        self.position = (int(moment['m10'] / moment['m00']), int(moment['m01'] / moment['m00']))
        self.ellipse = cv2.fitEllipse(self.contour) if len(self.contour) >= 5 else None
        self.area = cv2.contourArea(self.contour)
        self.area_mm = self.area * (scale ** 2)
        self.lightness = -1
        self.orientaton =  -1
        self.directionality = -1      

    def draw_ellipse(self, img_original):

        if self.ellipse is not None:
            cv2.ellipse(img_original, self.ellipse, (0,255,0), 2)

    def circularity(self):
        if self.ellipse:
            (x, y), (width, height), angle = self.ellipse
            return width / height
        else:
            return None

    def regularity(self):
        hull = cv2.convexHull(self.contour)
        hull_area = cv2.contourArea(hull)
        return self.area / hull_area
    
    def annotate(self, image):

        font = cv2.FONT_HERSHEY_SIMPLEX
        anotation = str(self.regularity()) + str(cv2.isContourConvex(self.contour))#+ " width: " + str(w) + "height: " + str(h)
        cv2.putText(image, anotation, (int(self.position[0] + 10), int(self.position[1] + 30)), font, 1, (0,255,255), 2, cv2.LINE_AA)

    def label(self):
        points = [x[0] for x in self.contour.tolist() ]
        label = {"points": points, "fill_color": None, "line_color": None, "label": "bloodstain"}
        # print(json.dumps(label, indent=4))
        return label
    
    
