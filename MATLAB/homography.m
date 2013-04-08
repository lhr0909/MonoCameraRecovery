function H = homography(img, square_size, corners)
%     figure(1); 
%     imshow(img); 
    % getting points from image 
%     [x1,y1]=ginput(1); 
%     [x2,y2]=ginput(1); 
%     [x3,y3]=ginput(1); 
%     [x4,y4]=ginput(1);
    % getting points from the corner_detector
    x1 = corners(1,1);
    y1 = corners(1,2);
    x2 = corners(2,1);
    y2 = corners(2,2);
    x3 = corners(3,1);
    y3 = corners(3,2);
    x4 = corners(4,1);
    y4 = corners(4,2);
    % setting up rectified points
    x11 = -square_size / 2;
    y11 = -square_size / 2;
    x22 = -square_size / 2;
    y22 =  square_size / 2;
    x33 =  square_size / 2;
    y33 =  square_size / 2;
    x44 =  square_size / 2;
    y44 = -square_size / 2;
    % calculate values from matrix
    A = [x1 y1 1  0  0 0 -x11*x1 -x11*y1 -x11;
          0  0 0 x1 y1 1 -y11*x1 -y11*y1 -y11;
         x2 y2 1  0  0 0 -x22*x2 -x22*y2 -x22;
          0  0 0 x2 y2 1 -y22*x2 -y22*y2 -y22;
         x3 y3 1  0  0 0 -x33*x3 -x33*y3 -x33;
          0  0 0 x3 y3 1 -y33*x3 -y33*y3 -y33;
         x4 y4 1  0  0 0 -x44*x4 -x44*y4 -x44;
          0  0 0 x4 y4 1 -y44*x4 -y44*y4 -y44;];
    H = null(A);
    H1 = [H(1) H(2) H(3); H(4) H(5) H(6); H(7) H(8) H(9)] ./ H(9);
    T1 = maketform('projective', H1');
    it1 = imtransform(img, T1);
%     imwrite(it1, filename);
    % imwrite(it1,'tile_floor_fixed1.ppm','ppm');
%     figure(5);
%     imshow(it1);
    H = H1;