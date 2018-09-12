import cv2
import numpy as np
path = '/media/cba62/Elements/Cropped Data/'
from parse_arguements import parse_args


def remove_rulers(image):
    '''finds lines in image, counts the number in each side of image by splitting in in half for left right then half horizontally for top bottom
    then it assumes that the lowest and highest are rulars then adds offsets and crops ??'''
    blur = cv2.GaussianBlur(image, (3,3), 0)
    grey = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(grey, 90, 100)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=0, maxLineGap=0)
    y_top_count = {}
    y_bottom_count = {}    
    x_left_count = {}
    x_right_count = {}
    max_x_len = (None, 0)
    
    h, w = grey.shape
    
    for line in lines:
        x1,y1,x2,y2 = line[0]
        max_x_len = (line, max(max_x_len[1], abs(x1 - x2))) if abs(x1 - x2) > max_x_len[1] else max_x_len
        y_low = max(y1, y2)
        if y_low < h / 2:
            y_top_count = line_count(y_low, y_top_count)
        else:
            y_bottom_count = line_count(y_low, y_bottom_count)
        if x1 < w / 2:
            x_left_count = line_count(x1, x_left_count)
        else:
            x_right_count = line_count(x1, x_right_count)
        if x2 < w / 2:
            x_left_count = line_count(x2, x_left_count)
        else:
            x_right_count = line_count(x2, x_right_count)
        
    sort_top_y = sorted(y_top_count, key=y_top_count.get)
    y = max(sort_top_y[-20:]) + 125
    print(y)
    
    sort_left_x = sorted(x_left_count, key=x_left_count.get)
    x = sort_left_x[-1] + 15
    print(x)

    sort_right_x = sorted(x_right_count, key=x_right_count.get)
    w2 = min(sort_right_x[-4:]) - 2 * x 
    print(w2)

    sort_bottom_y = sorted(y_bottom_count, key=y_bottom_count.get)
    h2 = min(sort_bottom_y[-4:]) - y - 15# remove_bottom(image[y:y+h, x:x+w2], y)
    if h2 > 0:
        h = h2

    print(h)
    crop_img = image[y:y+h, x:x+w2]
   
    return crop_img

def line_count(x1, x_count):
    if x1 in x_count:
        x_count[x1] += 1
    else:
        x_count[x1] = 1
    return x_count



def remove_bottom(no_ruler_crop, y):
    max_x_len = (None, 0)
    edges = cv2.Canny(no_ruler_crop, 90, 100)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=0, maxLineGap=0)
    for line in lines:
        x1,y1,x2,y2 = line[0]
        max_x_len = (line, max(max_x_len[1], abs(x1 - x2))) if abs(x1 - x2) > max_x_len[1] else max_x_len
    x1,y1,x2,y2 = max_x_len[0][0]
    return max(y1, y2) - y
    kernel = np.ones((3,3),np.uint8)


if __name__ == '__main__':
    args = parse_args() 
    print(args)
    filename = None if not args['filename'] else path + args['filename']
    full_path = args['full_path']
    if full_path:
        filename = full_path

    if not filename:
        print("No file selected")
    print("\nProcessing: " + filename)
    
    save_path = args['output_path']

    image = cv2.imread(filename)
    cropped = remove_rulers(image)
    name = (filename.split("/")[-1]).split('.')[0]
    path = save_path[:save_path.rfind('/')+1]

    cv2.imwrite(path + 'Makyee_shouting_' + name + '-cropped.jpg', cropped)