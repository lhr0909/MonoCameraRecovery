import cv2
import numpy

def filter_red_square(hsv, mask, size):
    img_square = numpy.zeros(hsv[:, :, 0].shape, numpy.uint8)
    #Filter out the small noise
    [contours, hierarchy] = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for i in xrange(len(contours)):
        area = cv2.contourArea(contours[i], False)
        if area >= size:
            cv2.drawContours(img_square,
                contours, i, [255, 255, 255],
                thickness=cv2.cv.CV_FILLED)
#    return img_square
    return cv2.blur(img_square, (51, 51))