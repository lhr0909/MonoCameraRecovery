#/usr/bin/env python

import numpy as np
import cv2

USAGE = '''
USAGE: calib.py [--save <filename>] [--debug <output path>] [--square_size] [<image mask>]
'''



if __name__ == '__main__':
    import sys, getopt
    from glob import glob

    args, img_mask = getopt.getopt(sys.argv[1:], '', ['save=', 'debug=', 'square_size='])
    args = dict(args)
    try: img_mask = img_mask[0]
    except: img_mask = 'raw/left*.png'
    img_names = glob(img_mask)
    debug_dir = args.get('--debug', 'debug')
    square_size = float(args.get('--square_size', 0.030)) # 30 millimeters

    pattern_size = (8, 5) # there is always these off by one issues!
    pattern_points = np.zeros( (np.prod(pattern_size), 3), np.float32 )
    pattern_points[:,:2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size

    obj_points = []
    img_points = []
    h, w = 0, 0
    for fn in img_names:
        print 'processing %s...' % fn,
        img = cv2.imread(fn, cv2.CV_LOAD_IMAGE_GRAYSCALE)
        h, w = img.shape[:2]
        found, corners = cv2.findChessboardCorners(img, pattern_size)
        if found:
            term = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 )
            cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)
        if debug_dir:
            vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            cv2.drawChessboardCorners(vis, pattern_size, corners, found)
            name = fn.split("\\")[1].split(".")[0]
            cv2.imwrite('%s/%s_debug.png' % (debug_dir, name), vis)
        if not found:
            print 'chessboard not found'
            continue
        img_points.append(corners.reshape(-1, 2))
        obj_points.append(pattern_points)

        print 'ok'

    rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(
        obj_points, img_points, (w, h), None, None, None, None)
    print "RMS:", rms
    print "camera matrix:\n", camera_matrix
    print "distortion coefficients: ", dist_coefs.ravel()
#    print "rotational vectors: ", rvecs
#    print "tranlational vectors: ", tvecs
    cv2.destroyAllWindows()

