import sys
import cv2
import numpy
import os
from PIL import Image
import numpy as np

def floodfill(im, grayimg, seed, color, tolerance=15):
    width, height = grayimg.size
    grayim = grayimg.load()
    start_color = grayim[seed]
    start_color = 49
    # print(start_color)

    mask_img = Image.new('L', grayimg.size, 255)
    mask = mask_img.load()
    count = 0
    work = [seed]
    while work:
        x, y = work.pop()
        im[x, y] = color
        for dx, dy in ((-1,0), (1,0), (0,-1), (0,1)):
            nx, ny = x + dx, y + dy
            if nx < 0 or ny < 0 or nx > width - 1 or ny > height - 1:
                continue
            if mask[nx, ny] and abs(grayim[nx, ny] - start_color) <= tolerance:
                mask[nx, ny] = 0
                work.append((nx, ny))
    return mask_img

img = Image.open(sys.argv[1]).convert('RGBA')
width, height = img.size
img_p = Image.new('RGBA', (width, height), img.getpixel((0, 0)))
img_p.paste(img)
img = img_p
img_g = img.convert('L')
width, height = img.size

im = img.load()
mask = floodfill(im, img_g, (3, 0), (0, 0, 0, 0), 15)

# seed_pt = (3, 0)
# mask = np.zeros((height+2, width+2), np.uint8)
# flags = 4
# flags |= cv2.FLOODFILL_FIXED_RANGE
# lo = 22
# hi = 36
# mask[:] = 0

# cv2.floodFill(numpy.array(img_g), mask, seed_pt, (0, 0, 0), (lo,)*3, (hi,)*3, flags)

mask = numpy.array(mask)
# se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
# mask = cv2.erode(mask, se)
# mask = cv2.GaussianBlur(mask, (3, 3), 1)
mask = Image.fromarray(mask)

result_bgcolor = (0, 0, 0, 255) # Change to match the color you wish.
result = Image.new('RGBA', (width, height), result_bgcolor)
result.paste(img_p, (0, 0), mask)

name = os.path.basename(sys.argv[1])
result.save('trans/' + name)