import numpy as np
from cv2 import cv2
import os
import imutils
# import pyimagesearch.transform import four_point_transform

def main():
    images = ['training_images/ktp-1.png',
          'training_images/ktp-2.png',
          'training_images/ktp-3.png',
          'training_images/ktp-4.png']
    for image in images:
        processKTP(image)

def processKTP(image_path):
    # load the image, compute the ratio of old vs new height, clone, and resize
    image = cv2.imread(image_path)
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height = 500)

    # do bitwise AND with pixels that are between the threshold
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([80, 0, 0])
    upper_blue = np.array([140, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    res = cv2.bitwise_and(hsv, hsv, mask = mask)

    # convert image to grayscale, blur it, and find edges
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # either white or black
    _, threshold = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # use canny edge detection algorithm
    # edged = cv2.Canny(threshold, 75, 200)

    contours,hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) != 0:
        # draw in blue the contours that were founded
        cv2.drawContours(threshold, contours, -1, 255, 3)

        # find the biggest countour (c) by the area
        contour = max(contours, key = cv2.contourArea)

        # smooth the contour into a convexhull
        hull = cv2.convexHull(contour)

        # draw the convexhull on the original image
        cv2.drawContours(image, [hull], -1, (255, 0, 0), 3)

        points = orderPoints(hull)
        (tl, tr, bl, br) = points
        cv2.circle(image, (tl[0], tl[1]), 5, (0,0,255), -1)
        cv2.circle(image, (tr[0], tr[1]), 5, (0,0,255), -1)
        cv2.circle(image, (bl[0], bl[1]), 5, (0,0,255), -1)
        cv2.circle(image, (br[0], br[1]), 5, (0,0,255), -1)

    # cv2.imshow("image", image)
    # cv2.imshow("res", res)
    # cv2.imshow("thres", threshold)
    # cv2.imshow("edged", edged)
    cv2.imwrite("results/" + image_path.replace("training_images/", ""), image)

def orderPoints(hull):
    pts = np.array(map(lambda x: x[0], hull))

    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype = "int32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    # sum here is x + y coordinate
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect

if __name__ == '__main__':
    main()
