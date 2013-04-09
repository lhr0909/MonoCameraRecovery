import numpy
from numpy import linalg

def recover_position(H, K):
    invK = linalg.inv(K)
    print invK
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
        [[2.64407914375522,  0.231720687559951, -690.523613388706],
         [-0.507121938721236, 2.59868620652448, -589.471296323130],
         [ 0.000490272463600770, -0.000498893118900209, 1.0]],
        numpy.float32)

    K = numpy.array(
        [[674.327013196338, 0.0, 476.778746813838],
         [0.0, 674.327013196338, 292.515323265311],
         [0.0, 0.0, 1.0]],
        numpy.float32)
    print recover_position(linalg.inv(H), K)