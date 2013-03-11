function video_source = camera()
    % stop video capturing for the previous run
    if (exist('vid', 'var') == 1)
        stop(vid);
        clear vid;
    end
    % % initialization of the system
    % clear all;
    % warning off;
    % clc;
    % webcam initialization
    fprintf('Initializing Webcam...');
    vid = videoinput('winvideo', 1, 'YUY2_640x480');
    src = getselectedsource(vid);
    % turn off all the auto adjustment settings
    src.BacklightCompensation = 'off';
    src.ExposureMode = 'manual';
    src.WhiteBalanceMode = 'manual';
    set(vid,'ReturnedColorSpace','rgb');
    % infinite trigger and allocate more memory for the camera
    vid.FramesPerTrigger = Inf;
    imaqmem(3000000000);
    start(vid);
    pause(0.5);
    fprintf('Done.\n');
    video_source = vid;
%     a = peekdata(vid, 1);
% %     imwrite(a, filename);
%     stop(vid);
%     clear vid;