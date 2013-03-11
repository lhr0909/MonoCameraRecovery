function van = estimateVanishingPoint(seg);
    A = [];
    for i = 1:size(seg,1)
        x1 = seg(i,1);
        y1 = seg(i,2);
        x2 = seg(i,3);
        y2 = seg(i,4);
        A = [A; [x1 y1 1] * [0 -1 y2; ...
                             1 0 -x2; ...
                             -y2 x2 0]];
    end
    [~, ~, v] = svd(A);
    van = v(:,3) ./ v(3,3);