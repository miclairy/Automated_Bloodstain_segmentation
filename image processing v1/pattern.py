import numpy as np

class Pattern:

    def __init__(self, stains=[]):
        self.stains = stains
        self.elliptical_stains = []
        for stain in self.stains:
            if stain.ellipse:
                self.elliptical_stains.append(stain)
        print("pancake", self.elliptical_stains)

    def convergence(self):
        intersects = []

        stains = sorted(self.elliptical_stains, key= lambda s: s.major_axis[0])
        for i in range(len(stains) - 1):
            axis = stains[i].major_axis
            if axis is not None:
                while i+1 < len(stains) and stains[i + 1].major_axis == None:
                    i += 1
                if i+1 >= len(stains):
                    break
                j = i + 1
                still_left = stains[j].major_axis[0][0] < axis[1][0]
                while  j < len(stains) and still_left:
                    intersect = self.line_intersection(axis, stains[j].major_axis)
                    if intersect:
                        intersects.append(intersect)
                    j += 1
                    while j < len(stains) and stains[j].major_axis == None :
                        j += 1
                    if j >= len(stains):
                        break
                    still_left = stains[j].major_axis[0][0] < axis[1][0] 
        print(intersects)
        # TODO work out what to do here and clean up the code!


    def line_intersection(self, line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) 

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            return None

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y
    
    def linearity(self):
        pass

    def distribution(self):
        pass