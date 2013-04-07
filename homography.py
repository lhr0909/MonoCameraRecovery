import numpy

def nullspace(A):
    eps = 1e-2
    u, s, vh = numpy.linalg.svd(A)
    print s
    print vh.shape
    null_space = numpy.compress(s <= eps, vh, axis=0)
    return null_space.T


def getHomography(corners):
    #fix corners
    corners_mean = numpy.mean(corners, axis=0)
    print corners
    new_corners = []
    for n in xrange(4):
        for i in xrange(corners.shape[0]):
            if corners[i,0] <= corners_mean[0] and corners[i,1] <= corners_mean[1] and len(new_corners) == 0:
                new_corners.append([corners[i,0], corners[i,1]])
                numpy.delete(corners, i, axis=0)
                break
            if corners[i,0] > corners_mean[0] and corners[i,1] <= corners_mean[1] and len(new_corners) == 1:
                new_corners.append([corners[i,0], corners[i,1]])
                numpy.delete(corners, i, axis=0)
                break
            if corners[i,0] > corners_mean[0] and corners[i,1] > corners_mean[1] and len(new_corners) == 2:
                new_corners.append([corners[i,0], corners[i,1]])
                numpy.delete(corners, i, axis=0)
                break
            if corners[i,0] <= corners_mean[0] and corners[i,1] > corners_mean[1] and len(new_corners) == 3:
                new_corners.append([corners[i,0], corners[i,1]])
                numpy.delete(corners, i, axis=0)
                break
    new_corners = numpy.array(new_corners, numpy.float32)
    c = new_corners
    L = 5
    sc = numpy.array([
        (-L/2, -L/2),
        (L/2, -L/2),
        (L/2, L/2),
        (-L/2, L/2)],numpy.float32)

    # H = null([x1 y1 1  0  0 0 -x11*x1 -x11*y1 -x11;
    #            0  0 0 x1 y1 1 -y11*x1 -y11*y1 -y11;
    #           x2 y2 1  0  0 0 -x22*x2 -x22*y2 -x22;
    #            0  0 0 x2 y2 1 -y22*x2 -y22*y2 -y22;
    #           x3 y3 1  0  0 0 -x33*x3 -x33*y3 -x33;
    #            0  0 0 x3 y3 1 -y33*x3 -y33*y3 -y33;
    #           x4 y4 1  0  0 0 -x44*x4 -x44*y4 -x44;
    #            0  0 0 x4 y4 1 -y44*x4 -y44*y4 -y44;]);

    M = numpy.array([
        [c[0,0], c[0,1], 1, 0, 0, 0, -sc[0,0]*c[0,0], -sc[0,0]*c[0,1], -sc[0,0]],
        [0, 0, 0, c[0,0], c[0,1], 1, -sc[0,1]*c[0,0], -sc[0,1]*c[0,1], -sc[0,1]],
        [c[1,0], c[1,1], 1, 0, 0, 0, -sc[1,0]*c[1,0], -sc[1,0]*c[0,1], -sc[1,0]],
        [0, 0, 0, c[1,0], c[1,1], 1, -sc[1,1]*c[1,0], -sc[1,1]*c[1,1], -sc[1,1]],
        [c[2,0], c[2,1], 1, 0, 0, 0, -sc[2,0]*c[2,0], -sc[2,0]*c[2,1], -sc[2,0]],
        [0, 0, 0, c[2,0], c[2,1], 1, -sc[2,1]*c[2,0], -sc[2,1]*c[2,1], -sc[2,1]],
        [c[3,0], c[3,1], 1, 0, 0, 0, -sc[3,0]*c[3,0], -sc[3,0]*c[3,1], -sc[3,0]],
        [0, 0, 0, c[3,0], c[3,1], 1, -sc[3,1]*c[3,0], -sc[3,1]*c[3,1], -sc[3,1]]],
    numpy.float32
    )
    ns = nullspace(M)
    print ns

if __name__ == "__main__":
    getHomography(numpy.array([[463,406],[235,109],[210,362],[498,142]], numpy.float32))