import cv2
import numpy
from numpy import linalg
from filter_red_square import filter_red_square
from get_corners import get_corners
from homography import getHomography
from recover_position import recover_position

cv2.namedWindow("MonoCameraRecovery", cv2.CV_WINDOW_AUTOSIZE)
camera = cv2.VideoCapture(0)

# Make sure you turn off the Auto White Balance,
# Auto Exposure, and Auto Backlight Compensation
# in the driver settings!

K = numpy.array(
    [[700.38176146, 0.0, 309.9551006],
     [0.0, 700.01361423, 279.4139976],
     [0.0, 0.0, 1.0]],
    numpy.float32)

def get_mask():
    #print numpy.average(hsv[:,:,2])
    #    mask = cv2.inRange(hsv,
    #        numpy.array([230, 135, 250], numpy.uint8),
    #        numpy.array([255, 165, 255], numpy.uint8))
    mask = cv2.inRange(hsv,
        numpy.array([230, 135, 200], numpy.uint8),
        numpy.array([255, 175, 255], numpy.uint8))
    #    mask = cv2.inRange(hsv,
    #        numpy.array([230, 185, 80], numpy.uint8),
    #        numpy.array([255, 250, 170], numpy.uint8))
    #    #open then close
    #se = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
    #mask = cv2.dilate(mask, se)
    #    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se)
    #    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, se)
    return mask

while True:
    [retval, img] = camera.read()
    #img = cv2.imread("raw/original.png")
    orig_img = numpy.copy(img)
    #convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
    mask = get_mask()

    img_square = filter_red_square(hsv, mask)
    #img_square = cv2.medianBlur(img_square, 51)

    #Corner Detection
    square_corners = get_corners(img, img_square)

    if len(square_corners) == 4:
        square_corners = numpy.array(square_corners, numpy.float32)
        #print square_corners
        H = getHomography(square_corners)
        #print H
        if H is not None:
            print recover_position(linalg.inv(H), K)


    cv2.imshow("MonoCameraRecovery", img)
    #cv2.imshow("MonoCameraRecovery", img_square)

    key = cv2.waitKey(1)
    if key == 13:
        cv2.imwrite('raw/original.png', orig_img)
        cv2.imwrite('raw/hsv.png', hsv)
        cv2.imwrite("raw/result.png", img)
        cv2.imwrite("raw/square.png", img_square)
        square_corners = numpy.array(square_corners, numpy.float32)
        #print square_corners
        H = getHomography(square_corners)
        #print H
        if H is not None:
            print recover_position(linalg.inv(H), K)
        break

camera.release()