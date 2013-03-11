% Based on these articles
% http://www.epixea.com/research/multi-view-coding-thesisse9.html
% http://mechatronics.ece.usu.edu/yqchen/paper/06C20_600042-final-paper.pdf
% http://en.wikipedia.org/wiki/Camera_resectioning

function [R, C, dist, angx, angy, angz, t] = recover_position(H, K)
    r1a = inv(K) * H(:,1);
    r2a = inv(K) * H(:,2);
    ta = inv(K) * H(:,3);
    r1 = r1a ./ norm(r1a);
    r2 = r2a ./ norm(r2a);
    r3a = cross(r1, r2);
    r3 = r3a ./ norm(r3a);
    R = [r1 r2 r3];
    t = ta ./ ((norm(r1a) + norm(r2a)) / 2);
%     t = ta;
%     C = -t;
    C = -(inv(R) * t);
    dist = norm(C);

    angy = atan2(-R(3,1), sqrt(R(1,1)^2 + R(2,1)^2));
    angz = atan2(R(2,1)/cos(angy), R(1,1)/cos(angy));
    angx = atan2(R(3,2)/cos(angy), R(3,3)/cos(angy));

    angz = angz/pi*180;
    angy = angy/pi*180;
    angx = angx/pi*180;