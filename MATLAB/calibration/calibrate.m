getLineSegs_myers
% segs = selectseg2(im, seglist);
load segments
showLineSegs

v1 = estimateVanishingPoint(seg1);
v2 = estimateVanishingPoint(seg2);
v3 = estimateVanishingPoint(seg3);

[w K] = estimateK_square_pixels(v1, v2, v3);
