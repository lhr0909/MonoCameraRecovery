function actual_corners = filter_red(im)
    boxFilter = ones(3, 3) ./ 9;
    boxFilter2 = ones(51, 51) ./ (51*51);
    im(:,:,1) = double(filter2(boxFilter, im(:,:,1), 'same'));
    im(:,:,2) = double(filter2(boxFilter, im(:,:,2), 'same'));
    im(:,:,3) = double(filter2(boxFilter, im(:,:,3), 'same'));
%     figure(1);
%     imshow(im);
    % imtool(im(:,:,1));
    % imtool(im(:,:,2));
    % imtool(im(:,:,3));
    imHSV = rgb2hsv(im);
%     figure(2);
%     imshow(imHSV);
    % imtool(imHSV(:,:,1));
    % imtool(imHSV(:,:,2));
    % imtool(imHSV(:,:,3));
    % figure(4);
    % imshow(im(:,:,1) - im(:,:,2) - im(:,:,3));
%      imtool(imHSV);
    mask_red_square = zeros(size(im, 1), size(im, 2));
    mask_red_square(find(((imHSV(:,:,1) > 0.94 & imHSV(:,:,1) < 0.99)) & (imHSV(:,:,2) > 0.45 & imHSV(:,:,2) < 0.65) & (imHSV(:,:,3) > 0.9))) = 1;
    % mask_red_square = imopen(mask_red_square, strel('square', 3));
    % mask_red_square = imclose(mask_red_square, strel('square', 3));
    % 
%      imtool(mask_red_square);
    imCount = bwlabel(mask_red_square, 8);
    count = max(max(imCount));
    % Getting rid of the small noise
    i = 1;
    while (i <= count)
        if (length(find(imCount == i)) < 500)
            mask_red_square(find(imCount == i)) = 0;
            imCount = bwlabel(mask_red_square, 8);
            count = max(max(imCount));
            i = 1;
        else
            i = i + 1;
        end
    end
     imtool(mask_red_square);
    % Grab Corners
    mask_red_square = double(filter2(boxFilter2, mask_red_square, 'same'));
    corners = corner(im(:,:,2));
    figure(4);
    imshow(im);
    hold on;
    plot(corners(:,1), corners(:,2),'g*');
    hold off;
    actual_corners = [];
    for i = 1:size(corners, 1)
        if (mask_red_square(corners(i,2), corners(i,1)) > 0)
            actual_corners = [actual_corners; [corners(i,1), corners(i,2)]];
        end
    end

    corners = actual_corners;
    if (size(corners, 1) < 4)
        return
    end
    % Find Order
    corner_mean = mean(corners);
%     disp(corner_mean);
    for i = 1:size(corners,1)
        if (corners(i,1) < corner_mean(1))
            if (corners(i,2) < corner_mean(2))
                actual_corners(1,:) = corners(i,:);
            else
                actual_corners(2,:) = corners(i,:);
            end
        else
            if (corners(i,2) < corner_mean(2))
                actual_corners(4,:) = corners(i,:);
            else
                actual_corners(3,:) = corners(i,:);
            end
        end
    end
%     figure(3);
%     imshow(mask_red_square);
%     figure(5);
%     imshow(im);
%     hold on;
%     plot(actual_corners(:,1), actual_corners(:,2),'b*');
%     hold off;
%     imwrite(mask_red_square, filename);