#!/usr/bin/env python

from PIL import Image
from lib import bresenham_line

# TODO: Normalize coordinates so image can be any size (reference image size was: 1936 x 1360)
# TODO: Read file name from argv

# Similarity formula taken from http://stackoverflow.com/a/26768008

SIMILARITY_THRESHOLD = 50

def luminance(pixel):
    return (0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])

def is_similar(pixel_a, pixel_b, threshold):
    return abs(luminance(pixel_a) - luminance(pixel_b)) < threshold

class SegmentStripe:
    def __init__(self, image, start, end):
        self.image = image
        self.start = start
        self.end = end

    def _get_pixels_to_check(self):
        return bresenham_line.get_line(self.start, self.end)

    def _check_pixel(self, pixel, fg_colors):
        on = 0

        for pixel_b in fg_colors:
            if is_similar(pixel, pixel_b, SIMILARITY_THRESHOLD):
                on = on + 1

        return (on / len(fg_colors) > 0.8)

    def is_on(self, bg_colors, fg_colors):
        on = 0
        off = 0

        for coords in self._get_pixels_to_check():
            pixel = self.image.getpixel(coords);

            if(self._check_pixel(pixel, fg_colors)):
                on = on + 1
            else:
                off = off + 1

        return (on > off)

class Digit:
    def __init__(self, segment_stripes, bg_colors, fg_colors):
        self.segment_stripes = segment_stripes
        self.bg_colors = bg_colors
        self.fg_colors = fg_colors

    def get_digit(self):
        return ''

class MinusSeg(Digit):
    def get_digit(self):
        if(self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors)):
            return '-'
        else:
            return ''

class TwoSeg(Digit):
    def get_digit(self):
        return '' # TODO: Determine 1 or 0

class PointSeg(Digit):
    def get_digit(self):
        if(self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors)):
            return '.'
        else:
            return ''

class SevenSeg(Digit):
    def get_digit(self):
        return '' # TODO: Determine number between 0-9 or off

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

im = Image.open("test_images/20170207_135313_pchh.jpg")
rgb_image = im.convert('RGB')

bg_colors = get_bg_colors(rgb_image)
fg_colors = get_fg_colors(rgb_image)

#print im.size
#
#print bg_colors
#print fg_colors

digits = [
    MinusSeg([
        SegmentStripe(rgb_image, (240, 322), (220, 412)) # Check this, guessed numbers
    ], bg_colors, fg_colors)
    # TODO: Add remaining digits (TwoSeg, SevenSeg, SevenSeg, PointSeg, SevenSeg)
]


for digit in digits:
    print digit.get_digit()

#if(seg.is_on(bg_colors, fg_colors)):
#    print "on!"
#else:
#    print "off :("