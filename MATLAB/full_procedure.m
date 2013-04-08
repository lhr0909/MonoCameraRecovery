clear all;
warning off;
clc;
load calibration_results;
im = imread('../raw/original.png');
corners = filter_red(im);
H = homography(im, 500, corners);
invH = inv(H);
[R, C, dist, angx, angy, angz, t] = recover_position(invH, K);
figure(6);
imshow(im);
hold on
plot(corners(:,1), corners(:,2),'b*');
text(50,50, ['\color{green}You are ', num2str(dist / 100), ' inches away from the square.'], 'FontSize', 20);
%         text(50,100, ['\color{green}', 'Rotation: ', num2str(angx), ', ' , num2str(angy), ', ' , num2str(angz)], 'FontSize', 20);
hold off