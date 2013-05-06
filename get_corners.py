import cv2

def get_corners(img, img_square):
#    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = img[:,:,0] #use the blue channel
    square_corners = []
    corners = cv2.goodFeaturesToTrack(img_gray, 100, 0.05, 30, useHarrisDetector=True, k=0.1)
    if corners is not None and corners.shape[0] > 0:
        for c in corners:
            #print img_square[c[0,1],c[0,0]]
            if img_square[c[0, 1], c[0, 0]] > 0:
                cv2.circle(img, tuple(c[0]), 5, [0, 255, 0], thickness=2)
                square_corners.append((c[0, 0], c[0, 1]))
    return square_corners