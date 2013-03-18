import SimpleCV
import cv
camera = SimpleCV.Camera(camera_index=0)
camera.loadCalibration("default")
print camera.getAllProperties()
while True:
    img = camera.getImageUndistort().smooth()
#    peaks = img.huePeaks()
#    hue = img.hueDistance(180).smooth('median').binarize(30)
#    blobs = hue.findBlobs(minsize=5000)
#    #blobs.draw(width=5)
#    if blobs:
#        blobs.image = img
#        for blob in blobs:
#            blob.drawMinRect(color=SimpleCV.Color.GREEN, width=5)
#    corners = img.findCorners()
#    if corners:
#        corners.image = img
#        for corner in corners:
#            corner.draw(color=SimpleCV.Color.BLUE, width=1)
#    img.show()
    imgcv = img.getMatrix()
    #create HSV image using OpenCV
    hsv = cv.CreateImage((imgcv.cols, imgcv.rows), cv.IPL_DEPTH_8U, 3)
    cv.CvtColor(imgcv, hsv, cv.CV_BGR2HSV)

    img2 = SimpleCV.Image(hsv)
    img2.show()