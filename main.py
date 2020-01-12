import numpy as np
from cv2 import cv2

BACKGROUND_THRESHOLD = 20

def main():
  img = cv2.imread('training_images/ktp-2.png')

  prepreprocessed_img = prepreprocess_image(img)
  cv2.imwrite('sample0.png', prepreprocessed_img)

  preprocessed_img = preprocess_image(prepreprocessed_img)
  cv2.imwrite('sample1.png', preprocessed_img)

  contours_sorted, contour_is_card = find_cards(preprocessed_img)

  card_contours = []
  for i in range(len(contours_sorted)):
    if contour_is_card[i] == 1:
      cv2.drawContours(img, [contours_sorted[i]], -1, (255, 0, 0), 2)
  cv2.imwrite('sample2.png', img)

  # if len(contours_sorted) != 0:
  #   cards = []

  #   for i in range(len(contours_sorted)):
  #     if contour_is_card[i] == 1:
  #       draw_results(img, preprocess_card(contours_sorted[i], img))
  # else:
  #   print('Contours not found!')

def prepreprocess_image(img):
  """
  Preprocess the image to only show blue in the image.
  We do this because KTP has a blue background
  """

  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  lower_blue = np.array([12, 12, 135])
  upper_blue = np.array([168, 168, 255])

  mask = cv2.inRange(hsv, lower_blue, upper_blue)

  res = cv2.bitwise_and(img, img, mask = mask)

  return res

def preprocess_image(img):
  """Grays, blurs, and thresholds the img"""

  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  blur = cv2.GaussianBlur(gray, (5, 5), 0)

  """
  The best threshold level depends on the ambient lighting conditions.
  For bright lighting, a high threshold must be used to isolate the cards
  from the background. For dim lighting, a low threshold must be used.
  To make the card detector independent of lighting conditions, the
  following adaptive threshold method is used.

  A background pixel in the center top of the image is sampled to determine
  its intensity. The adaptive threshold is set at THRESHOLD_ADDER higher
  than that. This allows the threshold to adapt to the lighting conditions
  """

  img_w, img_h = np.shape(img)[:2]
  background_level = gray[int(img_h/100)][int(img_w/2)] # 1% from top, 50% from side
  threshold_level = background_level + BACKGROUND_THRESHOLD

  _, threshold = cv2.threshold(blur, threshold_level, 255, cv2.THRESH_BINARY)

  return threshold

# generates a flattened image of the card
# returns contours, and boolean to indicate if the contour is a card
def find_cards(img):
  """
  Finds all card-sized contours in thresholded image. Returns the number
  of cards, and a list of card controus sorted from largest to smallest.
  """

  # Find contours and sort their indices by contour size
  contours, hierarchies = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  index_sort = sorted(range(len(contours)), key=lambda i : cv2.contourArea(contours[i]), reverse=True)

  # If there are no contours, do nothing
  if len(contours) == 0:
    return [], []

  # Otherwise, initialize empty sorted contour and hierarchy lists
  contours_sort = []
  hierarchies_sort = []
  contour_is_card = np.zeros(len(contours), dtype=int)

  # hierarchy array can be used to check if the contours have parents or not
  for i in index_sort:
    contours_sort.append(contours[i])
    hierarchies_sort.append(hierarchies[0][i])

  """
  Determine which of the contours are cards by applying the following criteria
  1. Smaller area than the maximum card size
  2. Bigger area than the minimum card size
  3. Have no parents
  4. Have four corners
  """
  for i in range(len(contours_sort)):
    size = cv2.contourArea(contours_sort[i])
    perimeter = cv2.arcLength(contours_sort[i], True)
    approx = cv2.approxPolyDP(contours_sort[i], 0.01*perimeter, True)

    if hierarchies_sort[i][3] == -1 and len(approx) == 4:
      contour_is_card[i] = 1

  return contours_sort, contour_is_card

def preprocess_card(img, contour):
  """
  Uses contour to find information about the card. 
  Returns flattened, re-sized, grayed image.
  Ref: http://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-tranform-example/
  """

  perimeter = cv2.arcLength(contour, True)
  approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
  points = np.float32(approx)

  x, y, w, h = cv2.boundingRect(contour)

  temp_rect = np.zeros((4, 2), dtype='float32')

  s = np.sum(points, axis = 2)

  tl = points[np.argmin(s)] 
  br = points[np.argmax(s)]

  diff = np.diff(points, axis = -1)
  
  tr = points[np.argmin(diff)]
  bl = points[np.argmax(diff)]

  # Need to create an array listing points in order of
  # [top left, top right, bottom right, bottom left]
  # before doing the perspective transform

  if w <= 0.8*h: # If card is vertically oriented
    temp_rect[0] = tl
    temp_rect[1] = tr
    temp_rect[2] = br
    temp_rect[3] = bl

  if w >= 1.2*h: # If card is horizontally oriented
    temp_rect[0] = bl
    temp_rect[1] = tl
    temp_rect[2] = tr
    temp_rect[3] = br

  # If the card is 'diamond' oriented, a different algorithm
  # has to be used to identify which point is top left, top right
  # bottom left, and bottom right.

  if w > 0.8*h and w < 1.2*h: #If card is diamond oriented
    # If furthest left point is higher than furthest right point,
    # card is tilted to the left.
    if pts[1][0][1] <= pts[3][0][1]:
      # If card is titled to the left, approxPolyDP returns points
      # in this order: top right, top left, bottom left, bottom right
      temp_rect[0] = pts[1][0] # Top left
      temp_rect[1] = pts[0][0] # Top right
      temp_rect[2] = pts[3][0] # Bottom right
      temp_rect[3] = pts[2][0] # Bottom left

      # If furthest left point is lower than furthest right point,
      # card is tilted to the right
      if pts[1][0][1] > pts[3][0][1]:
        # If card is titled to the right, approxPolyDP returns points
        # in this order: top left, bottom left, bottom right, top right
        temp_rect[0] = pts[0][0] # Top left
        temp_rect[1] = pts[3][0] # Top right
        temp_rect[2] = pts[2][0] # Bottom right
        temp_rect[3] = pts[1][0] # Bottom left

  maxWidth = 200
  maxHeight = 300

  # Create destination array, calculate perspective transform matrix,
  # and warp card image
  dst = np.array([[0,0],[maxWidth-1,0],[maxWidth-1,maxHeight-1],[0, maxHeight-1]], np.float32)
  M = cv2.getPerspectiveTransform(temp_rect,dst)
  warp = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
  warp = cv2.cvtColor(warp,cv2.COLOR_BGR2GRAY)

  return warp

def draw_result(img, card):
  return None

if __name__ == '__main__':
  main()
