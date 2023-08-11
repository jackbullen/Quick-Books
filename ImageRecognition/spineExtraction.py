import cv2
import pytesseract
import matplotlib.pyplot as plt
import os
import numpy as np
import PIL
from io import BytesIO
import math

def polarlines_to_startendpts(lines, ht, wd):
    ''' 
    Converts a line that is described by an angle and distance from origin
    to a line that is described by its start and end points.
    '''
    points = []

    for line in lines:
        
        # Set the r and theta values for this line.
        r, theta = line[0]
        
        # Unit vector in direction of closest point on the line.
        a = np.cos(theta)
        b = np.sin(theta)
        
        # Perp unit vector to above unit vector (aka the unit direction vector of the line)
        c = b
        d = -a
        
        # Closest point to origin that is on the line
        x0 = a * r
        y0 = b * r
        
        # Compute start and end points of the line by 
        x1 = int(x0 - (ht)*c)
        y1 = int(y0 - (ht)*d)
        x2 = int(x0 + (ht)*c)
        y2 = int(y0 + (ht)*d)
        
        points.append(((x1, y1), (x2, y2)))
    
    # Add a vertical line at the end and start of the image
    points.append(((wd, 0), (wd, ht)))
    points.append(((0, 0), (0, ht)))

    return points

def extend_lines(lines, ht):
    
    extended_lines = []
    for line in lines:
        # Grab coordinates of start and end points.
        ((x1, y1), (x2, y2)) = line
        
        # Compute the slope, if zero division then vertical line, set ticker.
        try:
            m = (y2-y1)/(x2-x1)
        except ZeroDivisionError:
            m = -999
        
        if m == -999:
            extended_lines.append(((x1, 0), (x2, ht))) #vertical line => use same x1 and x2
            
        else:
            # compute the offset for new points using the slope
            extra_x1_dist = y1/m
            extra_x2_dist = (ht-y2)/m

            new_x1 = x1 - extra_x1_dist
            new_x2 = x2 + extra_x2_dist

            extended_lines.append(((new_x1, 0), (new_x2, ht)))
        
    return extended_lines

def remove_overlapping_lines(points):
    previous_x = 0
    non_overlapping_pts = []
    for point in points:
        ((x1, y1), (x2, y2)) = point
        
        # Append the first point.
        if previous_x == 0:
            non_overlapping_pts.append(point)
            previous_x = x1

        # For all points after, make sure it's x value is a distance of
        # 25 pixels from the last appended point.
        elif abs(previous_x - x1) >= 25:
            non_overlapping_pts.append(point)
            previous_x = x1

    return non_overlapping_pts

def crop_spines(image, points):
    
    img = np.copy(image)
    ht, wd, _ = np.shape(img)
    
    prev_x1 = 0
    prev_x2 = 0
    
    cropped_spines = []
    
    for point in points:
        ((x1, y1), (x2, y2)) = point
        
        crop_pts = np.array([[prev_x2, 0],
                                [prev_x1, ht],
                                [x2, y2],
                                [x1, y1]])
        
        rect = cv2.boundingRect(crop_pts)
        x,y,w,h = rect
        cropped_spine = image[y: y + h, x: x + w].copy()
        
        cropped_spines.append(cropped_spine)
        
        prev_x1 = x1
        prev_x2 = x2
        
    return cropped_spines

def resize_img(image):
    ''' Resizes to width of 500 while maintaining the aspect ratio.  '''
    img = image.copy()
    img_ht, img_wd, _ = img.shape
    ratio = img_ht / img_wd
    new_width = 500
    new_height = math.ceil(new_width * ratio)
    img = cv2.resize(img, (new_width, new_height))
    return img

def extract_dividers(image):
    ''' Extracts the spine dividers from the image. '''

    img = np.copy(image)
    ht, wd, _ = img.shape

    # Blur the image to reduce noise
    img = cv2.GaussianBlur(img, (5,5), 0)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply edge detection on the image
    edges = cv2.Canny(gray, 50, 70)

    # Define a kernel to erode against for pronouncing vertical lines
    # and diminishing everything else.
    kernel = [[0, 0, 0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0]]
    kernel = np.array(kernel, dtype=np.uint8)

    erosion = cv2.erode(edges, kernel, iterations=1)

    # Compute the Houge lines
    lines = cv2.HoughLines(erosion, 1, np.pi/180, 100)
    if lines is None:  
        return []

    points = polarlines_to_startendpts(lines, ht, wd)
    points.sort(key=lambda x: x[0][0])
    non_overlapping_lines = remove_overlapping_lines(points)

    spine_dividers = extend_lines(non_overlapping_lines, ht)

    return spine_dividers

def extract_spine_imgs(image_path):
    ''' 
    Takes in the path to an image of a bookshelf.
    Returns the individual cv2 spine images. 
    '''
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise Exception(f"Error: Unable to read the image at '{image_path}'")  

    # Reduce the size of the image before detecting spines
    final_image = resize_img(image)

    # Detect the spine dividers
    final_points = extract_dividers(final_image)

    # Scale the spine dividers back to the size of the original image
    img_ht, img_wd, _ = image.shape
    resized_img_ht, resized_img_wd, _ = final_image.shape
    ratio_ht = img_ht / resized_img_ht
    ratio_wd = img_wd / resized_img_wd

    resized_points = []

    for point in final_points:
        ((x1, y1), (x2, y2)) = point

        # Scale up the coordinates to the size of the original image
        x1_original = int(x1 * ratio_wd)
        y1_original = int(y1 * ratio_ht)
        x2_original = int(x2 * ratio_wd)
        y2_original = int(y2 * ratio_ht)
        resized_points.append(((x1_original,y1_original), (x2_original, y2_original)))
        # Draw the line on the original image
        image = cv2.line(image, (x1_original, y1_original), (x2_original, y2_original), (0, 0, 255), 10)
    
    # Crop the image into individual spine images
    spines = crop_spines(image, resized_points)

    if spines is None:
        raise Exception("Error: Unable to extract spine images on file:", image_path)
    
    # Save the cropped images

    for i,img in enumerate(spines):
        if not cv2.imwrite('spine_imgs/'+image_path.split(".")[0].split("/")[-1]+str(i)+'.jpg', img):
            raise Exception("Could not write image")

    return spines, image