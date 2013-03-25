import cv2

cv2.namedWindow("TakeCalibPics", cv2.CV_WINDOW_AUTOSIZE)
camera = cv2.VideoCapture(0)

i = 0
while True:
    [retval, img] = camera.read()
    cv2.imshow("TakeCalibPics", img)
    key = cv2.waitKey(1)
    if key == 49:
        break
    elif key == 13:
        cv2.imwrite("raw/" + "left" + "%02d" % i + ".png", img)
        i += 1