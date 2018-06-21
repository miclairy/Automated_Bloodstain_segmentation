import cv2

class Stain:

    def __init__(self, contour):
        self.contour = contour
        self.ellipse = cv2.fitEllipse(self.contour) if len(self.contour) >= 5 else None
        self.area = cv2.contourArea(self.contour)  
        self.circularity = -1
        self.regularity = -1
        self.lightness = -1
        self.orientaton =  -1
        self.directionality = -1       

    def draw_ellipse(self, img_original):

        if self.ellipse is not None:
            cv2.ellipse(img_original, self.ellipse, (0,255,0), 2)
            
    
    def annotate(self, image):

        x,y,w,h = cv2.boundingRect(self.contour)
        font = cv2.FONT_HERSHEY_SIMPLEX
        anotation = str(self.area) #+ " width: " + str(w) + "height: " + str(h)
        cv2.putText(image, anotation, (int(x + 10), int(y + 30)), font, 1, (0,255,255), 2, cv2.LINE_AA)
