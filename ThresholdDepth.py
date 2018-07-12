import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def nothing(x):
    pass

img = cv.imread('gradient.png',0)
# webcam
cap = cv.VideoCapture(2)

# setup UI
cv.namedWindow('Controls', cv.WINDOW_NORMAL)
cv.namedWindow('Controls2', cv.WINDOW_NORMAL)
cv.createTrackbar('Min','Controls', 0, 255,nothing)
cv.createTrackbar('Max','Controls2', 0, 255,nothing)


while(1):

    # get key
    k = cv.waitKey(30) & 0xff
    print('key pressed is:',k)

    # load webcam
    ret, frame = cap.read()
    # convert to grayscale for openCV operations
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # setup UI
    minPixel = cv.getTrackbarPos('Min', 'Controls')
    maxPixel = cv.getTrackbarPos('Max', 'Controls2')
    # apply threshold
    ret, thresh1 = cv.threshold(gray, minPixel, maxPixel, cv.THRESH_BINARY)

    cv.imshow('gray', gray)
    cv.imshow('thresh1', thresh1)
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()

def createKeySliderBinding(label, keyDown, keyUp):

    print('calling create keySlider')
    obj = None
    obj.label = label
    obj.keyDown = keyDown
    obj.keyUp = keyUp
    return obj
