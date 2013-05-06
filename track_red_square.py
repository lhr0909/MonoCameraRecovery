import cv2
import visual
import numpy
from numpy import linalg
from filter_red_square import filter_red_square
from get_corners import get_corners
from homography import getHomography
from recover_position import recover_position

check_box = False
box_left = 0
box_top = 0
box_right = 0
box_bot = 0

mask_low = numpy.array([240, 115, 240], numpy.uint8)
mask_high = numpy.array([255, 135, 255], numpy.uint8)

def mouseDrag(evt, x, y, flags, *param):
    global box_left, box_top, box_right, box_bot, check_box
    if evt == cv2.EVENT_LBUTTONDOWN:
        print x, y, "down"
        box_left = x
        box_top = y
    if evt == cv2.EVENT_LBUTTONUP:
        print x, y, "up"
        box_right = x
        box_bot = y
        check_box = True



cv2.namedWindow("MonoCameraRecovery", cv2.CV_WINDOW_AUTOSIZE)
cv2.setMouseCallback("MonoCameraRecovery", mouseDrag, 0)
camera = cv2.VideoCapture(0)

square = visual.box(pos=(0, 0, 0), size=(4.0, 4.0, 0.1), color=visual.color.red)
cam_arrow1 = visual.arrow(pos=(0, 0, 5), axis=(0, 0, -1), shaftwidth=1, color=visual.color.green)
cam_arrow2 = visual.arrow(pos=(0, 0, 5), axis=(0, 1, 0), shaftwidth=1, color=visual.color.green)

# Make sure you turn off the Auto White Balance,
# Auto Exposure, and Auto Backlight Compensation
# in the driver settings!

K = numpy.array(
    [[700.38176146, 0.0, 309.9551006],
     [0.0, 700.01361423, 279.4139976],
     [0.0, 0.0, 1.0]],
    numpy.float32)


def ll(m, thres):
    #lower_limit
    return 0 if m - thres < 0 else int(m) - thres

def ul(m, thres):
    #upper_limit
    return 255 if m + thres > 255 else int(m) + thres

def set_mask(box_left, box_top, box_right, box_bot):
    global mask_low, mask_high, check_box
    print "checking"
    print box_left, box_top, box_right, box_bot
    img_crop = numpy.copy(img[box_top:box_bot + 1, box_left:box_right + 1, :])
    square.color = (
        numpy.mean(img_crop[:, :, 2]) / float(255),
        numpy.mean(img_crop[:, :, 1]) / float(255),
        numpy.mean(img_crop[:, :, 0]) / float(255)
        )
    img_crop_hsv = cv2.cvtColor(img_crop, cv2.COLOR_BGR2HSV_FULL)
    cv2.imwrite("raw/crop.png", img_crop_hsv)
    mean0 = numpy.mean(img_crop_hsv[:, :, 0])
    mean1 = numpy.mean(img_crop_hsv[:, :, 1])
    mean2 = numpy.mean(img_crop_hsv[:, :, 2])
    print mean0, mean1, mean2
    mask_low = numpy.array([ll(mean0, 20), ll(mean1, 20), ll(mean2, 20)], numpy.uint8)
    mask_high = numpy.array([ul(mean0, 20), ul(mean1, 20), ul(mean2, 20)], numpy.uint8)
    print mask_low, mask_high
    check_box = False

def get_mask(hsv):
    global mask_low, mask_high
    mask = cv2.inRange(hsv, mask_low, mask_high)
    #    #open then close
    #se = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
    #mask = cv2.dilate(mask, se)
    #    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se)
    #    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, se)
    return mask

capture = True
orig_img = None

while True:
    if capture:
        [retval, img] = camera.read()
        orig_img = numpy.copy(img)
    else:
        img = numpy.copy(orig_img)

    #img = cv2.imread("raw/original.png")
    #convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)

    if check_box:
        set_mask(box_left, box_top, box_right, box_bot)

    mask = get_mask(hsv)

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
            R, C = recover_position(linalg.inv(H), K)
            print numpy.linalg.norm(C), C
            cam_arrow1.pos = (C[0], -C[1], -C[2])
            cam_arrow2.pos = (C[0], -C[1], -C[2])
            cam_arrow1.axis = tuple(numpy.dot(R, numpy.array([0,0,-1], numpy.float32)).tolist())
            cam_arrow2.axis = tuple(numpy.dot(R, numpy.array([0,1,0], numpy.float32)).tolist())



    cv2.imshow("MonoCameraRecovery", img)
#    cv2.imshow("MonoCameraRecovery", img[:,:,0])
    #cv2.imshow("MonoCameraRecovery", img_square)

    visual.sleep(0.0001)
    key = cv2.waitKey(1)
#    if key == 13:
#        cv2.imwrite('raw/original.png', orig_img)
#        cv2.imwrite('raw/hsv.png', hsv)
#        cv2.imwrite("raw/result.png", img)
#        cv2.imwrite("raw/square.png", img_square)
#    elif key == 49:
#        capture = not capture

    if visual.scene.kb.keys:
        s = visual.scene.kb.getkey()
        print s
        if s == '1':
            capture = not capture
        elif s == '\n':
            cv2.imwrite('raw/original.png', orig_img)
            cv2.imwrite('raw/hsv.png', hsv)
            cv2.imwrite("raw/result.png", img)
            cv2.imwrite("raw/square.png", img_square)
        elif s == "esc":
            break


camera.release()
quit()