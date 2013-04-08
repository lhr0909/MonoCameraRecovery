import cv2
import numpy
from homography import getHomography
from recover_position import recover_position

cv2.namedWindow("MonoCameraRecovery", cv2.CV_WINDOW_AUTOSIZE)
camera = cv2.VideoCapture(0)

# Make sure you turn off the Auto White Balance,
# Auto Exposure, and Auto Backlight Compensation
# in the driver settings!

#TODO: auto checking background lighting and adjust the threshold

K = numpy.array(
    [[700.38176146, 0.0, 309.9551006],
     [0.0, 700.01361423, 279.4139976],
     [0.0, 0.0, 1.0]],
    numpy.float32)

while True:
    #[retval, img] = camera.read()
    img = cv2.imread("raw/original.png")
    orig_img = numpy.copy(img)
    #convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)

    #print numpy.average(hsv[:,:,2])

    mask = cv2.inRange(hsv,
        numpy.array([230, 135, 250], numpy.uint8),
        numpy.array([255, 165, 255], numpy.uint8))

#    #open then close
#    se = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
#    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se)
#    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, se)

    img_square = numpy.zeros(img[:,:,0].shape, numpy.uint8)

    #Filter out the small noise
    [contours, hierarchy] = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for i in xrange(len(contours)):
        area = cv2.contourArea(contours[i], False)
        if area >= 13000:
            cv2.drawContours(img_square,
                contours, i, [255, 255, 255],
                thickness=cv2.cv.CV_FILLED)

    img_square = cv2.blur(img_square, (75,75))
    #img_square = cv2.medianBlur(img_square, 51)

    #Corner Detection
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(img_gray, 100, 0.1, 50)
    square_corners = []
    if corners.shape[0] > 0:
        for c in corners:
            #print img_square[c[0,1],c[0,0]]
            if img_square[c[0,1],c[0,0]] > 0:
                cv2.circle(img, tuple(c[0]), 5, [0, 255, 0], thickness=2)
                square_corners.append((c[0,0], c[0,1]))


    cv2.imshow("MonoCameraRecovery", img)
    #cv2.imshow("MonoCameraRecovery", img_square)

    key = cv2.waitKey(1)
    if key == 13:
        cv2.imwrite('raw/original.png', orig_img)
        cv2.imwrite('raw/hsv.png', hsv)
        cv2.imwrite("raw/result.png", img)
        cv2.imwrite("raw/square.png", img_square)
        square_corners = numpy.array(square_corners, numpy.float32)
        print square_corners
        H = getHomography(square_corners)
        print H
        print recover_position(H, K)
        break

camera.release()