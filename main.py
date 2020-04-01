import numpy as np
from cv2 import cv2
import os
import imutils
# import pyimagesearch.transform import four_point_transform

def main():
  # load the image, compute the ratio of old vs new height, clone, and resize
  image = cv2.imread('training_images/ktp-1.png')
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

    hull = cv2.convexHull(contour)

    cv2.drawContours(image, [hull], -1, (255, 0, 0), 3)

  print("step 1: edge detection")
  # cv2.imshow("image", image)
  # cv2.imshow("res", res)
  # cv2.imshow("thres", threshold)
  # cv2.imshow("edged", edged)
  cv2.imshow("result", image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

  cv2.waitKey(1)

if __name__ == '__main__':
  main()
