import numpy as np
from cv2 import cv2

def main():
    img = cv2.imread('training_images/ktp-1.png')
    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    print(v[2][4])
    value = 130 - v[0][0]
    if value > 0:
        hsv[:, :, 2] += value
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        cv2.imwrite('img1.png', img)
    else:
        cv2.imwrite('img1.png', img)

    # blur
    b_im = cv2.GaussianBlur(img, (5, 5), 0)
    cv2.imwrite('img2.png', b_im)

    # to grayscale
    gray_im = cv2.cvtColor(b_im, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('img3.png', gray_im)

    # threshold
    _, thres_im = cv2.threshold(gray_im, 115, 255, cv2.THRESH_BINARY)
    cv2.imwrite('img4.png', thres_im)

    # dilation and erosion
    de_im = cv2.erode(thres_im, None, iterations=10)
    de_im = cv2.dilate(de_im, None, iterations=10)
    cv2.imwrite('img5.png', de_im)

    # ims = gray_im.filter(ImageFilter.SHARPEN)

    # cv2.imwrite('tmp/img2.png', ims)

def main2():
    img = cv2.imread('training_images/ktp-1.png')

    # convert to grayscale
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imwrite('img0.png', grayscale)

    # # compute the Scharr gradient magnitude representation of the images
    # # in both the x and y direction
    # ddepth = cv2.CV_32F
    # gradX = cv2.Sobel(grayscale, ddepth=ddepth, dx=1, dy=0, ksize=-1)
    # gradY = cv2.Sobel(grayscale, ddepth=ddepth, dx=0, dy=1, ksize=-1)

    # # subtract the y-gradient from the x-gradient
    # gradient = cv2.subtract(gradX, gradY)
    # gradient = cv2.convertScaleAbs(gradient)

    # # blur and threshold the image
    # blurred = cv2.blur(gradient, (9, 9))
    # (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

    # construct a closing kernel and apply it to the thresholded image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (27, 9))
    closed = cv2.morphologyEx(grayscale, cv2.MORPH_CLOSE, kernel)

    cv2.imwrite('img1.png', closed)

    # perform a series of erosions and dilations
    eroded = cv2.erode(closed, None, iterations = 10)
    dilated = cv2.dilate(eroded, None, iterations = 10)

    cv2.imwrite('img2.png', dilated)

    # find contours
    contours = cv2.findContours(
      dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    contours = contours[1]

    print(contours)
    for x in range(len(contours)):
        contour = contours[x]

        # compute the rotated bounding box of the largest contour
        rect = cv2.minAreaRect(contour)
        box = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
        box = numpy.int0(box)

        # draw a bounding box arounded the detected barcode and display the image
        cv2.drawContours(img, [box], -1, (255, 0, 0), 3)

if __name__ == '__main__':
  main2()
