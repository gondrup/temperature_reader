#!/usr/bin/env python

from PIL import Image, ImageDraw
from tempocr import segments
import sys

# TODO: Normalize coordinates so image can be any size (reference image size was: 1936 x 1360)
# TODO: Read file name from argv
# TODO: Fix perspective and pre-crop image:

def get_bg_colors(image):
    colors = []

    colors.append(image.getpixel((612, 252)))
    colors.append(image.getpixel((594, 489)))
    colors.append(image.getpixel((1026, 244)))
    colors.append(image.getpixel((1008, 494)))
    colors.append(image.getpixel((1456, 246)))
    colors.append(image.getpixel((1437, 478)))
    colors.append(image.getpixel((1760, 210)))

    return colors

def get_fg_colors(image):
    colors = []

    # Percent symbol
    colors.append(image.getpixel((1770, 1128)))

    # Celcius symbol
    colors.append(image.getpixel((1804, 360)))
    colors.append(image.getpixel((1738, 422)))
    colors.append(image.getpixel((1728, 562)))
    colors.append(image.getpixel((1792, 630)))

    return colors

# Open the source image

#im = Image.open("test_images/20170209_135025_pc.jpg")
im = Image.open("test_images/out/test.png")
rgb_image = im.convert('RGB')

# Get the BG and FG colours from known points on the image

bg_colors = get_bg_colors(rgb_image)
fg_colors = get_fg_colors(rgb_image)

# Define the known digits/segments

digits = [
    segments.MinusSeg([
        segments.SegmentStripe(rgb_image, (240, 322), (220, 412)) # Check this, guessed numbers
    ], bg_colors, fg_colors),
    segments.TwoSeg([
        segments.SegmentStripe(rgb_image, (93, 176), (114, 177)), # Check this, guessed numbers
        segments.SegmentStripe(rgb_image, (99, 84), (118, 86)) # Check this, guessed numbers
    ], bg_colors, fg_colors),
    segments.SevenSeg([
        segments.SegmentStripe(rgb_image, (634, 80), (636, 170)),
        segments.SegmentStripe(rgb_image, (716, 240), (795, 245)),
        segments.SegmentStripe(rgb_image, (701, 497), (774, 503)),
        segments.SegmentStripe(rgb_image, (594, 573), (592, 661)),
        segments.SegmentStripe(rgb_image, (430, 483), (505, 493)),
        segments.SegmentStripe(rgb_image, (452, 232), (520, 240)),
        segments.SegmentStripe(rgb_image, (615, 325), (615, 413)),
    ], bg_colors, fg_colors),
    segments.SevenSeg([
        segments.SegmentStripe(rgb_image, (1045, 80), (1047, 170)),
        segments.SegmentStripe(rgb_image, (1127, 240), (1206, 245)),
        segments.SegmentStripe(rgb_image, (1112, 497), (1185, 503)),
        segments.SegmentStripe(rgb_image, (1005, 573), (1003, 661)),
        segments.SegmentStripe(rgb_image, (841, 483), (916, 493)),
        segments.SegmentStripe(rgb_image, (863, 232), (931, 240)),
        segments.SegmentStripe(rgb_image, (1026, 325), (1026, 413))
    ], bg_colors, fg_colors),
    segments.PointSeg([
        segments.SegmentStripe(rgb_image, (1210, 614), (1211, 660)),
    ], bg_colors, fg_colors),
    segments.SevenSeg([
        segments.SegmentStripe(rgb_image, (1480, 80), (1482, 170)),
        segments.SegmentStripe(rgb_image, (1562, 240), (1641, 245)),
        segments.SegmentStripe(rgb_image, (1547, 497), (1620, 503)),
        segments.SegmentStripe(rgb_image, (1440, 573), (1438, 661)),
        segments.SegmentStripe(rgb_image, (1276, 483), (1351, 493)),
        segments.SegmentStripe(rgb_image, (1298, 232), (1366, 240)),
        segments.SegmentStripe(rgb_image, (1461, 325), (1461, 413))
    ], bg_colors, fg_colors)
]

# Print parsed temperature


temperature = ''
for digit in digits:
    temperature += digit.get_digit()

print temperature


'''
# Draw lines on image to stdout
for digit in digits:
    digit.draw_on_image()

rgb_image.save(sys.stdout, "PNG")
'''