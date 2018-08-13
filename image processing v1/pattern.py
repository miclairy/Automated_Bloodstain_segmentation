import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.stats import kde
import cv2


class Pattern:

    def __init__(self, stains=[]):
        self.stains = stains
        self.elliptical_stains = []
        self.image = None
        for stain in self.stains:
            if stain.ellipse:
                self.elliptical_stains.append(stain)
    
    def add_stain(self, stain):
        self.stains.append(stain)
        if stain.major_axis != None:
            self.elliptical_stains.append(stain)

    def convergence(self):
        height, width = self.image.shape[:2]
        intersects = []
        stains = sorted(self.elliptical_stains, key= lambda s: s.major_axis[0])
        for i in range(len(stains) - 1):
            axis = stains[i].major_axis
            j = i + 1
            still_left = stains[j].major_axis[0][0] < axis[1][0]
            while  j < len(stains) - 1 and still_left:
                intersect = self.line_intersection(axis, stains[j].major_axis)
                if intersect and intersect[0] < width and intersect[1] < height and intersect[0] > 0 and intersect[1] > 0:
                    intersects.append(intersect)
                j += 1
                still_left = stains[j].major_axis[0][0] < axis[1][0] 

        self.plot_convergence(intersects)

    def plot_convergence(self, intersects):

        x_values = [x[0] for x in intersects]
        y_values = [x[1] for x in intersects]
        fig = plt.figure(1, figsize=(12, 12))
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)
        # ax3 = fig.add_subplot(223)

        x = x_values
        y = y_values
        height, width = self.image.shape[:2]

        # Plotting a regular scatter plot
        ax1.plot(x, y, '*', markersize=3, color='g')
        ax1.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB), extent=[0, width, height, 0], aspect='auto') 
        ax1.set_xlim(0, max(x_values))
        ax1.set_ylim(max(y_values), 0)
        ax1.set_title("Scatter Plot of Directional Major Axis Intersections")
        ax1.set_xlabel("pixels")
        ax1.set_ylabel("pixels")

        
        nbins = 300
        k = kde.gaussian_kde([x,y])
        xi, yi = np.mgrid[min(x):max(x):nbins*1j, min(y):max(y):nbins*1j]
        point_density = k(np.vstack([xi.flatten(), yi.flatten()]))

        most_dense = np.unravel_index(np.argmax(point_density), point_density.shape) # index
        convergence_point = (xi.flatten()[most_dense], yi.flatten()[most_dense])
        print("most dense point", convergence_point)

        bound = point_density[most_dense] * 0.6
        most_dense_points_x = xi.flatten()[np.where(point_density > bound)]
        most_dense_points_y = yi.flatten()[np.where(point_density > bound)]
        
        
        box_min_x = min(most_dense_points_x)
        box_min_y = min(most_dense_points_y)
        box_width = max(most_dense_points_x) - box_min_x 
        box_height = max(most_dense_points_y) - box_min_y
        
        ax2.set_ylim(max(y_values), 0)
        ax2.set_xlim(0, max(x_values))
        
        # Make the plot
        im = ax2.pcolormesh(xi, yi, point_density.reshape(xi.shape))
        box = patches.Rectangle((box_min_x, box_min_y), box_width, box_height, linewidth=1, edgecolor='black', facecolor='none')
        ax2.add_patch(box)

        # heatmap, xedges, yedges = np.histogram2d(x, y, bins=50)
        # extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

        # im = ax3.imshow(heatmap.T, extent=extent, origin='lower', aspect='auto', interpolation='bilinear')
        # ax3.set_ylim(max(y_values), 0)
        # ax3.set_xlim(0, max(x_values))
        ax2.set_title("Heat Map of Convergence")
        ax2.set_xlabel("pixels")
        ax2.set_ylabel("pixels")
        cb = fig.colorbar(im, ax=ax2)
        cb.set_label('mean number of intersections')

        plt.show()

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
        stain_centers_x = np.array([stain.position[0] for stain in self.stains])
        stain_centers_y = np.array([stain.position[1] for stain in self.stains])
        
        xp = np.linspace(0, max(stain_centers_x))
        fitted = np.polyfit(stain_centers_x, stain_centers_y, 2)
        poly = np.poly1d(fitted)
        _fitted_plot = plt.plot(stain_centers_x, stain_centers_y, '.', xp, poly(xp), '-')
        plt.ylim(max(stain_centers_y), 0)

        y_fit = poly(stain_centers_x)                         
        yi = np.sum(stain_centers_y) / len(stain_centers_y)          
        ssreg = np.sum((y_fit - yi) ** 2)   
        sstot = np.sum((stain_centers_y - yi) ** 2)   
        r_squared = ssreg / sstot

        plt.text(100, 100, "R^2 = " + str(r_squared))
        plt.show()
        
        return poly, r_squared

            

    def distribution(self):
        pass