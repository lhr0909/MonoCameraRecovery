import cv2

cv2.namedWindow("Calibration", cv2.CV_WINDOW_AUTOSIZE)
camera = cv2.VideoCapture(0)
flags = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE + cv2.CALIB_CB_FAST_CHECK

i = 0
while True:
    [retval, img] = camera.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #print img.shape
    found, corners = cv2.findChessboardCorners(img, (9, 6), flags=flags)
    print found

    if found:
        cv2.drawChessboardCorners(img, (9, 6), corners, found)

    cv2.imshow("Calibration", img)

    key = cv2.waitKey(1)
    if key == 49:
        break
    elif key == 13:
        cv2.imwrite("left" + "%02d" % i + ".png", img)
        i += 1