#!/usr/bin/env python
# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2

if __name__ == '__main__':
    import sys
    try:
        fn = sys.argv[1]
    except:
        fn = '../data/fruits.jpg'

    img = cv2.imread(fn, True)
    if img is None:
        print('Failed to load image file:', fn)
        sys.exit(1)

    h, w = img.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    seed_pt = (3, 0)
    fixed_range = True
    connectivity = 4

    flooded = img.copy()
    mask[:] = 0
    lo = 22
    hi = 36
    flags = connectivity
    if fixed_range:
        flags |= cv2.FLOODFILL_FIXED_RANGE
    cv2.floodFill(flooded, mask, seed_pt, (255, 255, 255), (lo,)*3, (hi,)*3, flags)
    cv2.imshow('floodfill', flooded)
    #  cv2.waitKey(0)
    #  cv2.destroyAllWindows()
    cv2.imwrite('messigray.png',flooded)