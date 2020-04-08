import numpy as np
from cv2 import cv2
import os
import imutils
from imutils.object_detection import non_max_suppression
import argparse
import pytesseract
import time

def main(args):
    images = ['training_images/ktp-1.png',
          'training_images/ktp-2.png',
          'training_images/ktp-3.png',
          'training_images/ktp-4.png',
          'training_images/ktp-5.png',
          'training_images/ktp-6.png',
          'training_images/ktp-7.png',
          'training_images/ktp-8.png']
    for image in images:
        processKTP(image, args['width'], args['height'], 
                args['east'], args['min_confidence'], args['padding'])

def processKTP(image_path, width, height, east_path, min_confidence, padding):
    # load the image, compute the ratio of old vs new height, clone, and resize
    image = cv2.imread(image_path)

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

        # get 4 corners of the contour
        points = orderPoints(hull)
        # (tl, tr, bl, br) = points
        # cv2.circle(image, (tl[0], tl[1]), 5, (0,0,255), -1)
        # cv2.circle(image, (tr[0], tr[1]), 5, (0,0,255), -1)
        # cv2.circle(image, (bl[0], bl[1]), 5, (0,0,255), -1)
        # cv2.circle(image, (br[0], br[1]), 5, (0,0,255), -1)

        # transform to flattened image (bird view)
        flat = fourPointTransform(image, points)

        res = detectText(flat, width, height, east_path, min_confidence, padding)

        cv2.imwrite('results/' + image_path.replace('training_images/', ''), res)
    else:
        print('Error processing image')

def orderPoints(hull):
    pts = np.array(map(lambda x: x[0], hull))

    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype = 'float32')

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

# reference: https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
def fourPointTransform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    (tl, tr, br, bl) = pts

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    # use pythagorean theorem to get the distance
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a 'birds eye view',
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = 'float32')

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(pts, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    return warped

def detectText(image, width, height, east_path, min_confidence, padding):
    orig = image.copy()
    (origH, origW) = image.shape[:2]
    (newH, newW) = (args['height'], args['width'])
    
    # calculate ratio to new height and width
    rW = origW / float(newW)
    rH = origH / float(newH)

    # resize the image using the ratio
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]

    # define two output layer names for the EAST detector model that we
    # are interested -- the first is the output probabilities and the second
    # can be used to derive the bounding box coordinates of text
    layerNames = [
            # uses Sigmoid activation to give us probability of a region
            # containing text or not
            'feature_fusion/Conv_7/Sigmoid', 
            # output feature map that represents the geometry of the image
            'feature_fusion/concat_3']

    # load the pre-trained EAST text detector
    print('[INFO] loading EAST text detector...')
    net = cv2.dnn.readNet(east_path)

    # construct a blob from the image and then perform a forward pass of the
    # model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H), 
            (123.68, 116.78, 103.94), swapRB=True, crop=False)
    start = time.time()
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    end = time.time()

    # show timing information on text prediction
    print('[INFO] text detection took {:.6f} seconds'.format(end-start))

    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the geometrical
        # data used to derived potential bounding box coordinates that
        # surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]

        # loop over the number of columns
        for x in range(0, numCols):
            if scoresData[x] < min_confidence:
                continue

            # compute the offset factor as our resulting feature maps will
            # be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)

            # extract the rotation angle for the prediction and then 
            # compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # use the geometry volume to derive the width and height of
            # the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]

            # compute both the starting and ending (x, y)-coordinates for
            # the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            # add the bounding box coordinates and probability score to
            # our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])

    boxes = non_max_suppression(np.array(rects), probs=confidences)

    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective ratios
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)

        # in order to obtain a better OCR of the text we can potentially 
        # apply a bitof padding surrounding the bounding box -- here we are
        # computing the deltas in both the x and y directions
        dX = int((endX - startX) * padding)
        dY = int((endY - startY) * padding)

        # apply padding to each side of the bounding box, respectively
        startX = max(0, startX - dX)
        startY = max(0, startY - dY)
        endX = min(origW, endX + dX)
        endY = min(origH, endY + dY)

        # draw the boudning box on the image
        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

    return orig

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-e', '--east', type=str, help='path to input image')
    ap.add_argument('-c', '--min-confidence', type=float, default=0.5)
    # EAST text requires that input image dimensions be multiples of 32
    ap.add_argument('-W', '--width', type=int, default=640)
    ap.add_argument('-H', '--height', type=int, default=640)
    ap.add_argument('-P', '--padding', type=float, default=0.05)
    args = vars(ap.parse_args())

    main(args)
