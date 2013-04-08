import numpy

def nullspace(A, eps=2**-52):
    '''
    Nullspace function
    copied from the MATLAB null() function
    using only the orthonormal basis
    '''
    m, n = A.shape
    u, S, V = numpy.linalg.svd(A)

    if m > 1:
        s = numpy.diag(S)
        s = s[numpy.nonzero(s)]
        smax = numpy.max(s)
    elif m == 1:
        s = S[0,0]
        smax = s
    else:
        s = 0
        smax = 0

    tol = max(m, n) * smax * eps
    r = sum(s > tol)
    return V[:, r:]


def getHomography(corners, L=500):
    if corners.shape[0] == 4 and corners.shape[1] == 2:
        #fix corners
        corners_mean = numpy.mean(corners, axis=0)
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
        print new_corners
        c = new_corners
        sc = numpy.array([
            (-L/2, -L/2),
            (L/2, -L/2),
            (L/2, L/2),
            (-L/2, L/2)],numpy.float32)

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
        ns = nullspace(M).T
        ns = numpy.divide(ns, ns[0,8])
        ns = numpy.array(
            [[ns[0,0], ns[0,1], ns[0,2]],
             [ns[0,3], ns[0,4], ns[0,5]],
             [ns[0,6], ns[0,7], ns[0,8]]], numpy.float32)
        return ns
    else:
        return None

if __name__ == "__main__":
    H = getHomography(numpy.array([[463,406],[235,109],[210,362],[498,142]], numpy.float32))
    print H