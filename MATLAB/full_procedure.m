if (exist('vid', 'var') == 1)
    flushdata(vid);
    stop(vid);
    clear vid;
end
clear all;
warning off;
clc;
load calibration_results;
while 1
    x = 1;
    vid = camera();
    while x < 15
        im = peekdata(vid, 1);
        corners = filter_red(im);
        if (size(corners, 1) < 4)
            x = x + 1;
            continue
        end
        H = homography(im, 500, corners);
        invH = inv(H);
        [R, C, dist, angx, angy, angz, t] = recover_position(invH, K);
        figure(6);
        imshow(im);
        hold on
        plot(corners(:,1), corners(:,2),'b*');
        text(50,50, ['\color{green}', num2str(x), ': You are ', num2str(dist / 100), ' inches away from the square.'], 'FontSize', 20);
%         text(50,100, ['\color{green}', 'Rotation: ', num2str(angx), ', ' , num2str(angy), ', ' , num2str(angz)], 'FontSize', 20);
        hold off
        x = x + 1;
    %     flushdata(vid);
    end
    flushdata(vid);
    stop(vid);
    clear vid;
end
% im = imread('sample_square_3.png');