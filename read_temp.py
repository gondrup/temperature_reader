#!/usr/bin/env python

from PIL import Image
from lib import bresenham_line

# TODO: Normalize coordinates so image can be any size (reference image size was: 1936 x 1360)
# TODO: Read file name from argv

# Similarity formula taken from http://stackoverflow.com/a/26768008

SIMILARITY_THRESHOLD = 70

def luminance(pixel):
    return (0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])

def get_difference(pixel_a, pixel_b):
    return abs(luminance(pixel_a) - luminance(pixel_b))

def is_similar(pixel_a, pixel_b, threshold):
    return get_similarity(pixel_a, pixel_b) < threshold

class SegmentStripe:
    def __init__(self, image, start, end):
        self.image = image
        self.start = start
        self.end = end

    def _get_pixels_to_check(self):
        return bresenham_line.get_line(self.start, self.end)

    def _check_pixel(self, pixel, bg_colors, fg_colors):
        bg_values = []
        fg_values = []

        for pixel_b in bg_colors:
            #print 'bg', pixel, pixel_b

            bg_values.append(get_difference(pixel, pixel_b))

        for pixel_b in fg_colors:
            #print 'fg', pixel, pixel_b

            fg_values.append(get_difference(pixel, pixel_b))

        bg_average = sum(bg_values) / len(bg_values)
        fg_average = sum(fg_values) / len(fg_values)

        #print bg_values, fg_values

        return (fg_average < bg_average)

    def is_on(self, bg_colors, fg_colors):
        on = 0
        off = 0

        for coords in self._get_pixels_to_check():
            pixel = self.image.getpixel(coords);

            if(self._check_pixel(pixel, bg_colors, fg_colors)):
                on = on + 1
            else:
                off = off + 1

        #print 'on:', on, 'off:', off

        return (on > off)

    def is_off(self, bg_colors, fg_colors):
        return not(self.is_on(bg_colors, fg_colors))

class Digit:
    def __init__(self, segment_stripes, bg_colors, fg_colors):
        self.segment_stripes = segment_stripes
        self.bg_colors = bg_colors
        self.fg_colors = fg_colors

    def get_digit(self):
        return ''

class MinusSeg(Digit):
    def get_digit(self):
        # 0 = Minus

        if(self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors)):
            return '-'
        else:
            return ''

class TwoSeg(Digit):
    def get_digit(self):
        # 0 = Top
        # 1 = Bottom

        if(
            self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors)
            and self.segment_stripes[1].is_on(self.bg_colors, self.fg_colors)
        ):
            return '1'
        else:
            return ''

class PointSeg(Digit):
    def get_digit(self):
        # 0 = Dot

        if(self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors)):
            return '.'
        else:
            return ''

class SevenSeg(Digit):
    def _is_0(self):
        return (
            self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors) # 0 = Top
            and self.segment_stripes[1].is_on(self.bg_colors, self.fg_colors) # 1 = Top Right
            and self.segment_stripes[2].is_on(self.bg_colors, self.fg_colors) # 2 = Bottom Right
            and self.segment_stripes[3].is_on(self.bg_colors, self.fg_colors) # 3 = Bottom
            and self.segment_stripes[4].is_on(self.bg_colors, self.fg_colors) # 4 = Bottom Left
            and self.segment_stripes[5].is_on(self.bg_colors, self.fg_colors) # 5 = Too Left
            and self.segment_stripes[6].is_off(self.bg_colors, self.fg_colors) # 6 = Middle
        )

    def _is_1(self):
        return (
            self.segment_stripes[0].is_off(self.bg_colors, self.fg_colors) # 0 = Top
            and self.segment_stripes[1].is_on(self.bg_colors, self.fg_colors) # 1 = Top Right
            and self.segment_stripes[2].is_on(self.bg_colors, self.fg_colors) # 2 = Bottom Right
            and self.segment_stripes[3].is_off(self.bg_colors, self.fg_colors) # 3 = Bottom
            and self.segment_stripes[4].is_off(self.bg_colors, self.fg_colors) # 4 = Bottom Left
            and self.segment_stripes[5].is_off(self.bg_colors, self.fg_colors) # 5 = Too Left
            and self.segment_stripes[6].is_off(self.bg_colors, self.fg_colors) # 6 = Middle
        )

    def _is_2(self):
        return (
            self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors) # 0 = Top
            and self.segment_stripes[1].is_on(self.bg_colors, self.fg_colors) # 1 = Top Right
            and self.segment_stripes[2].is_off(self.bg_colors, self.fg_colors) # 2 = Bottom Right
            and self.segment_stripes[3].is_on(self.bg_colors, self.fg_colors) # 3 = Bottom
            and self.segment_stripes[4].is_on(self.bg_colors, self.fg_colors) # 4 = Bottom Left
            and self.segment_stripes[5].is_off(self.bg_colors, self.fg_colors) # 5 = Too Left
            and self.segment_stripes[6].is_on(self.bg_colors, self.fg_colors) # 6 = Middle
        )

    def _is_3(self):
        return (
            self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors) # 0 = Top
            and self.segment_stripes[1].is_on(self.bg_colors, self.fg_colors) # 1 = Top Right
            and self.segment_stripes[2].is_on(self.bg_colors, self.fg_colors) # 2 = Bottom Right
            and self.segment_stripes[3].is_on(self.bg_colors, self.fg_colors) # 3 = Bottom
            and self.segment_stripes[4].is_off(self.bg_colors, self.fg_colors) # 4 = Bottom Left
            and self.segment_stripes[5].is_off(self.bg_colors, self.fg_colors) # 5 = Too Left
            and self.segment_stripes[6].is_on(self.bg_colors, self.fg_colors) # 6 = Middle
        )

    def _is_4(self):
        return (
            self.segment_stripes[0].is_off(self.bg_colors, self.fg_colors) # 0 = Top
            and self.segment_stripes[1].is_on(self.bg_colors, self.fg_colors) # 1 = Top Right
            and self.segment_stripes[2].is_on(self.bg_colors, self.fg_colors) # 2 = Bottom Right
            and self.segment_stripes[3].is_off(self.bg_colors, self.fg_colors) # 3 = Bottom
            and self.segment_stripes[4].is_off(self.bg_colors, self.fg_colors) # 4 = Bottom Left
            and self.segment_stripes[5].is_on(self.bg_colors, self.fg_colors) # 5 = Too Left
            and self.segment_stripes[6].is_on(self.bg_colors, self.fg_colors) # 6 = Middle
        )

    def _is_5(self):
        return (
            self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors) # 0 = Top
            and self.segment_stripes[1].is_off(self.bg_colors, self.fg_colors) # 1 = Top Right
            and self.segment_stripes[2].is_on(self.bg_colors, self.fg_colors) # 2 = Bottom Right
            and self.segment_stripes[3].is_on(self.bg_colors, self.fg_colors) # 3 = Bottom
            and self.segment_stripes[4].is_off(self.bg_colors, self.fg_colors) # 4 = Bottom Left
            and self.segment_stripes[5].is_on(self.bg_colors, self.fg_colors) # 5 = Too Left
            and self.segment_stripes[6].is_on(self.bg_colors, self.fg_colors) # 6 = Middle
        )

    def _is_6(self):
        return (
            self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors) # 0 = Top
            and self.segment_stripes[1].is_off(self.bg_colors, self.fg_colors) # 1 = Top Right
            and self.segment_stripes[2].is_on(self.bg_colors, self.fg_colors) # 2 = Bottom Right
            and self.segment_stripes[3].is_on(self.bg_colors, self.fg_colors) # 3 = Bottom
            and self.segment_stripes[4].is_on(self.bg_colors, self.fg_colors) # 4 = Bottom Left
            and self.segment_stripes[5].is_on(self.bg_colors, self.fg_colors) # 5 = Too Left
            and self.segment_stripes[6].is_on(self.bg_colors, self.fg_colors) # 6 = Middle
        )

    def _is_7(self):
        return (
            self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors) # 0 = Top
            and self.segment_stripes[1].is_on(self.bg_colors, self.fg_colors) # 1 = Top Right
            and self.segment_stripes[2].is_on(self.bg_colors, self.fg_colors) # 2 = Bottom Right
            and self.segment_stripes[3].is_off(self.bg_colors, self.fg_colors) # 3 = Bottom
            and self.segment_stripes[4].is_off(self.bg_colors, self.fg_colors) # 4 = Bottom Left
            and self.segment_stripes[5].is_off(self.bg_colors, self.fg_colors) # 5 = Too Left
            and self.segment_stripes[6].is_off(self.bg_colors, self.fg_colors) # 6 = Middle
        )

    def _is_8(self):
        return (
            self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors) # 0 = Top
            and self.segment_stripes[1].is_on(self.bg_colors, self.fg_colors) # 1 = Top Right
            and self.segment_stripes[2].is_on(self.bg_colors, self.fg_colors) # 2 = Bottom Right
            and self.segment_stripes[3].is_on(self.bg_colors, self.fg_colors) # 3 = Bottom
            and self.segment_stripes[4].is_on(self.bg_colors, self.fg_colors) # 4 = Bottom Left
            and self.segment_stripes[5].is_on(self.bg_colors, self.fg_colors) # 5 = Too Left
            and self.segment_stripes[6].is_on(self.bg_colors, self.fg_colors) # 6 = Middle
        )

    def _is_9(self):
        return (
            self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors) # 0 = Top
            and self.segment_stripes[1].is_on(self.bg_colors, self.fg_colors) # 1 = Top Right
            and self.segment_stripes[2].is_on(self.bg_colors, self.fg_colors) # 2 = Bottom Right
            and self.segment_stripes[3].is_on(self.bg_colors, self.fg_colors) # 3 = Bottom
            and self.segment_stripes[4].is_off(self.bg_colors, self.fg_colors) # 4 = Bottom Left
            and self.segment_stripes[5].is_on(self.bg_colors, self.fg_colors) # 5 = Too Left
            and self.segment_stripes[6].is_on(self.bg_colors, self.fg_colors) # 6 = Middle
        )

    def get_digit(self):
        i = 0
        for seg in self.segment_stripes:
            print i, ': '
            if(seg.is_on(self.bg_colors, self.fg_colors)):
                print 'on'
            else:
                print 'off'

            i = i + 1

        if(self._is_0()):
            return '0'
        elif(self._is_1()):
            return '1'
        elif(self._is_2()):
            return '2'
        elif(self._is_3()):
            return '3'
        elif(self._is_4()):
            return '4'
        elif(self._is_5()):
            return '5'
        elif(self._is_6()):
            return '6'
        elif(self._is_7()):
            return '7'
        elif(self._is_8()):
            return '8'
        elif(self._is_9()):
            return '9'
        else:
            return ''

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

im = Image.open("test_images/20170207_135313_pc.jpg")
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
    ], bg_colors, fg_colors),
    TwoSeg([
        SegmentStripe(rgb_image, (93, 176), (114, 177)), # Check this, guessed numbers
        SegmentStripe(rgb_image, (99, 84), (118, 86)) # Check this, guessed numbers
    ], bg_colors, fg_colors),
    SevenSeg([
        SegmentStripe(rgb_image, (234, 28), (224, 60)),
        SegmentStripe(rgb_image, (253, 85), (281, 87)),
        SegmentStripe(rgb_image, (247, 175), (273, 178)),
        SegmentStripe(rgb_image, (210, 202), (209, 233)),
        SegmentStripe(rgb_image, (158, 171), (178, 174)),
        SegmentStripe(rgb_image, (160, 82), (183, 84)),
        SegmentStripe(rgb_image, (217, 115), (217, 145))
    ], bg_colors, fg_colors)
    # TODO: Add remaining digits (TwoSeg, SevenSeg, SevenSeg, PointSeg, SevenSeg)
]


for digit in digits:
    print digit.get_digit()

#if(seg.is_on(bg_colors, fg_colors)):
#    print "on!"
#else:
#    print "off :("