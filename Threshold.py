import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def nothing(x):
    pass


def createKeySliderBinding(label, keyDown, keyUp, value, valueMin, valueMax):
    print('calling create keySlider')
    # creating an empty object
    # https://stackoverflow.com/questions/19476816/creating-an-empty-object-in-python
    obj = lambda: None
    obj.label = label
    obj.keyDown = keyDown
    obj.keyUp = keyUp
    obj.value = value
    obj.valueMin = valueMin
    obj.valueMax = valueMax
    print("creating keybinding for '" + label + "' ")
    return obj

def keyPressedKeySlider( keySlider, k ):
    newValue = keySlider.value
    bChanged = False
    if k == keySlider.keyDown:
        newValue -=1
        bChanged = True
        if newValue < keySlider.valueMin:
            newValue = keySlider.valueMin
    elif k == keySlider.keyUp:
        newValue +=1
        bChanged = True
        if newValue > keySlider.valueMax:
            newValue = keySlider.valueMax

    if bChanged == True:
        print(keySlider.label, "changed to", newValue)
    keySlider.value = newValue
    return keySlider

img = cv.imread('gradient.png',0)
# webcam
cap = cv.VideoCapture(2)

# setup UI
'''
cv.namedWindow('Controls', cv.WINDOW_NORMAL)
cv.namedWindow('Controls2', cv.WINDOW_NORMAL)
cv.createTrackbar('Min','Controls', 0, 255,nothing)
cv.createTrackbar('Max','Controls2', 0, 255,nothing)
'''

minPixel = createKeySliderBinding("minThreshold",113 , 119, 12, 0, 255)
print(minPixel.value)
maxPixel = createKeySliderBinding("maxThreshold",97 , 115, 255, 0, 255)

while 1:
    # get key
    k = cv.waitKey(30)

    if k > 0:
        global minPixel
        keyPressedKeySlider( minPixel, k)
        keyPressedKeySlider( maxPixel, k)

       # global maxPixel
       # maxPixel = keyPressedKeySlider( minPixel, k)
       # print('doing things')

    # load webcam
    ret, frame = cap.read()
    # convert to grayscale for openCV operations
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # setup UI
    # minPixel = cv.getTrackbarPos('Min', 'Controls')
    # maxPixel = cv.getTrackbarPos('Max', 'Controls2')
    # apply threshold
    ret, thresh1 = cv.threshold(gray, minPixel.value, maxPixel.value, cv.THRESH_BINARY)

    cv.imshow('gray', gray)
    cv.imshow('thresh1', thresh1)
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()


