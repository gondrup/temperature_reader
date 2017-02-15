#!/usr/bin/env python

from PIL import Image, ImageDraw
from lib import bresenham_line
import sys

# TODO: Normalize coordinates so image can be any size (reference image size was: 1936 x 1360)
# TODO: Read file name from argv

# Similarity formula taken from http://stackoverflow.com/a/26768008

SIMILARITY_THRESHOLD = 18

def luminance(pixel):
    return (0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])

def get_difference(pixel_a, pixel_b):
    return abs(luminance(pixel_a) - luminance(pixel_b))

def is_similar(pixel_a, pixel_b, threshold):
    return get_difference(pixel_a, pixel_b) < threshold

# http://stackoverflow.com/questions/19914509/python-pil-pixel-rgb-color-to-hex
def rgb2hex(pixel):
    return '#{:02x}{:02x}{:02x}'.format(pixel[0], pixel[1], pixel[2])

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
            bg_values.append(get_difference(pixel, pixel_b))

        for pixel_b in fg_colors:
            fg_values.append(get_difference(pixel, pixel_b))

        bg_average = sum(bg_values) / len(bg_values)
        fg_average = sum(fg_values) / len(fg_values)

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

        return (on > off)

    def is_off(self, bg_colors, fg_colors):
        return not(self.is_on(bg_colors, fg_colors))

    def draw_on_image(self, fill):
        draw = ImageDraw.Draw(self.image)
        draw.line([self.start, self.end], fill=fill, width=2)
        del draw

class Digit:
    def __init__(self, segment_stripes, bg_colors, fg_colors):
        self.segment_stripes = segment_stripes
        self.bg_colors = bg_colors
        self.fg_colors = fg_colors

    def get_digit(self):
        return ''

    def draw_on_image(self):
        for seg in self.segment_stripes:
            seg.draw_on_image("lightgreen")

class MinusSeg(Digit):
    def get_digit(self):
        if(self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors)): # 0 = Minus
            return '-'
        else:
            return ''

class TwoSeg(Digit):
    def get_digit(self):
        if(
            self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors) # 0 = Top
            and self.segment_stripes[1].is_on(self.bg_colors, self.fg_colors) # 1 = Bottom
        ):
            return '1'
        else:
            return ''

class PointSeg(Digit):
    def get_digit(self):
        if(self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors)): # 0 = Dot
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

# Open the source image

#im = Image.open("test_images/20170209_135025_pc.jpg")
im = Image.open("test_images/out/test.png")
rgb_image = im.convert('RGB')

# Get the BG and FG colours from known points on the image

bg_colors = get_bg_colors(rgb_image)
fg_colors = get_fg_colors(rgb_image)

# Define the known digits/segments

digits = [
    MinusSeg([
        SegmentStripe(rgb_image, (240, 322), (220, 412)) # Check this, guessed numbers
    ], bg_colors, fg_colors),
    TwoSeg([
        SegmentStripe(rgb_image, (93, 176), (114, 177)), # Check this, guessed numbers
        SegmentStripe(rgb_image, (99, 84), (118, 86)) # Check this, guessed numbers
    ], bg_colors, fg_colors),
    SevenSeg([
        SegmentStripe(rgb_image, (634, 80), (636, 170)),
        SegmentStripe(rgb_image, (716, 240), (795, 245)),
        SegmentStripe(rgb_image, (701, 497), (774, 503)),
        SegmentStripe(rgb_image, (594, 573), (592, 661)),
        SegmentStripe(rgb_image, (430, 483), (505, 493)),
        SegmentStripe(rgb_image, (452, 232), (520, 240)),
        SegmentStripe(rgb_image, (615, 325), (615, 413)),
    ], bg_colors, fg_colors),
    SevenSeg([
        SegmentStripe(rgb_image, (1045, 80), (1047, 170)),
        SegmentStripe(rgb_image, (1127, 240), (1206, 245)),
        SegmentStripe(rgb_image, (1112, 497), (1185, 503)),
        SegmentStripe(rgb_image, (1005, 573), (1003, 661)),
        SegmentStripe(rgb_image, (841, 483), (916, 493)),
        SegmentStripe(rgb_image, (863, 232), (931, 240)),
        SegmentStripe(rgb_image, (1026, 325), (1026, 413))
    ], bg_colors, fg_colors),
    PointSeg([
        SegmentStripe(rgb_image, (1210, 614), (1211, 660)),
    ], bg_colors, fg_colors),
    SevenSeg([
        SegmentStripe(rgb_image, (1480, 80), (1482, 170)),
        SegmentStripe(rgb_image, (1562, 240), (1641, 245)),
        SegmentStripe(rgb_image, (1547, 497), (1620, 503)),
        SegmentStripe(rgb_image, (1440, 573), (1438, 661)),
        SegmentStripe(rgb_image, (1276, 483), (1351, 493)),
        SegmentStripe(rgb_image, (1298, 232), (1366, 240)),
        SegmentStripe(rgb_image, (1461, 325), (1461, 413))
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