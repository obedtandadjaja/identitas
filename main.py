import numpy as np
from cv2 import cv2

def main():
    img = cv2.imread("training_images/ktp-1.png")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imwrite("tmp/sample_gray.png", img_gray)

    ret, image_binary = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    image_not = cv2.bitwise_not(image_binary)

    erode_kernel = np.ones((3, 1), np.uint8)
    image_erode = cv2.erode(image_not, erode_kernel, iterations = 5)

    dilate_kernel = np.ones((5,5), np.uint8)
    image_dilate = cv2.dilate(image_erode, dilate_kernel, iterations=5)

    kernel = np.ones((3, 3), np.uint8)
    image_closed = cv2.morphologyEx(image_dilate, cv2.MORPH_CLOSE, kernel)
    image_open = cv2.morphologyEx(image_closed, cv2.MORPH_OPEN, kernel)

    image_not = cv2.bitwise_not(image_open)
    image_not = cv2.adaptiveThreshold(image_not, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)

    image_dilate = cv2.dilate(image_not, np.ones((2, 1)), iterations=1)
    image_dilate = cv2.dilate(image_dilate, np.ones((2, 10)), iterations=1)

    image, contours = cv2.findContours(image_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # if w > 30 and h > 10:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imwrite("tmp/sample.png", img)

if __name__ == "__main__":
  main()
