import numpy
from numpy import linalg

def recover_position(H, K):
    invK = linalg.inv(K)
    #get rotational matrix R
    R0raw = numpy.dot(invK, H[:,0])
    R1raw = numpy.dot(invK, H[:,1])
    R2raw = numpy.cross(R0raw, R1raw)
    R0 = R0raw / linalg.norm(R0raw)
    R1 = R1raw / linalg.norm(R1raw)
    R2 = R2raw / linalg.norm(R2raw)
    Traw = numpy.dot(invK, H[:,2])
    T = Traw / ((linalg.norm(R0raw) + linalg.norm(R1raw)) / 2)
    R = numpy.array([
        [R0[0], R1[0], R2[0]],
        [R0[1], R1[1], R2[1]],
        [R0[2], R1[2], R2[2]],
        ], numpy.float32)
    C = -linalg.inv(R).dot(T)
    return linalg.norm(C)

if __name__ == "__main__":
    H = numpy.array(
        [[  1.77615881e-01,  1.80893600e-01, -9.42133713e+01],
         [ -1.16202652e-01, -1.79449499e-01,  7.77696381e+01],
         [ -3.55348364e-02,  2.49527674e-02,  1.00000000e+00]],
        numpy.float32)

    K = numpy.array(
        [[700.38176146, 0.0, 309.9551006],
         [0.0, 700.01361423, 279.4139976],
         [0.0, 0.0, 1.0]],
        numpy.float32)
    print recover_position(H, K)