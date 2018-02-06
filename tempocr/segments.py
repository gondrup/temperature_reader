from tempocr.color import compare, convert
from vendor.bresenham_line import bresenham_line
from PIL import Image, ImageDraw

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
            bg_values.append(compare.get_difference(pixel, pixel_b))

        for pixel_b in fg_colors:
            fg_values.append(compare.get_difference(pixel, pixel_b))

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
            and self.segment_stripes[5].is_on(self.bg_colors, self.fg_colors) # 5 = Top Left
            and self.segment_stripes[6].is_off(self.bg_colors, self.fg_colors) # 6 = Middle
        )

    def _is_1(self):
        return (
            self.segment_stripes[0].is_off(self.bg_colors, self.fg_colors) # 0 = Top
            and self.segment_stripes[1].is_on(self.bg_colors, self.fg_colors) # 1 = Top Right
            and self.segment_stripes[2].is_on(self.bg_colors, self.fg_colors) # 2 = Bottom Right
            and self.segment_stripes[3].is_off(self.bg_colors, self.fg_colors) # 3 = Bottom
            and self.segment_stripes[4].is_off(self.bg_colors, self.fg_colors) # 4 = Bottom Left
            and self.segment_stripes[5].is_off(self.bg_colors, self.fg_colors) # 5 = Top Left
            and self.segment_stripes[6].is_off(self.bg_colors, self.fg_colors) # 6 = Middle
        )

    def _is_2(self):
        return (
            self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors) # 0 = Top
            and self.segment_stripes[1].is_on(self.bg_colors, self.fg_colors) # 1 = Top Right
            and self.segment_stripes[2].is_off(self.bg_colors, self.fg_colors) # 2 = Bottom Right
            and self.segment_stripes[3].is_on(self.bg_colors, self.fg_colors) # 3 = Bottom
            and self.segment_stripes[4].is_on(self.bg_colors, self.fg_colors) # 4 = Bottom Left
            and self.segment_stripes[5].is_off(self.bg_colors, self.fg_colors) # 5 = Top Left
            and self.segment_stripes[6].is_on(self.bg_colors, self.fg_colors) # 6 = Middle
        )

    def _is_3(self):
        return (
            self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors) # 0 = Top
            and self.segment_stripes[1].is_on(self.bg_colors, self.fg_colors) # 1 = Top Right
            and self.segment_stripes[2].is_on(self.bg_colors, self.fg_colors) # 2 = Bottom Right
            and self.segment_stripes[3].is_on(self.bg_colors, self.fg_colors) # 3 = Bottom
            and self.segment_stripes[4].is_off(self.bg_colors, self.fg_colors) # 4 = Bottom Left
            and self.segment_stripes[5].is_off(self.bg_colors, self.fg_colors) # 5 = Top Left
            and self.segment_stripes[6].is_on(self.bg_colors, self.fg_colors) # 6 = Middle
        )

    def _is_4(self):
        return (
            self.segment_stripes[0].is_off(self.bg_colors, self.fg_colors) # 0 = Top
            and self.segment_stripes[1].is_on(self.bg_colors, self.fg_colors) # 1 = Top Right
            and self.segment_stripes[2].is_on(self.bg_colors, self.fg_colors) # 2 = Bottom Right
            and self.segment_stripes[3].is_off(self.bg_colors, self.fg_colors) # 3 = Bottom
            and self.segment_stripes[4].is_off(self.bg_colors, self.fg_colors) # 4 = Bottom Left
            and self.segment_stripes[5].is_on(self.bg_colors, self.fg_colors) # 5 = Top Left
            and self.segment_stripes[6].is_on(self.bg_colors, self.fg_colors) # 6 = Middle
        )

    def _is_5(self):
        return (
            self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors) # 0 = Top
            and self.segment_stripes[1].is_off(self.bg_colors, self.fg_colors) # 1 = Top Right
            and self.segment_stripes[2].is_on(self.bg_colors, self.fg_colors) # 2 = Bottom Right
            and self.segment_stripes[3].is_on(self.bg_colors, self.fg_colors) # 3 = Bottom
            and self.segment_stripes[4].is_off(self.bg_colors, self.fg_colors) # 4 = Bottom Left
            and self.segment_stripes[5].is_on(self.bg_colors, self.fg_colors) # 5 = Top Left
            and self.segment_stripes[6].is_on(self.bg_colors, self.fg_colors) # 6 = Middle
        )

    def _is_6(self):
        return (
            self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors) # 0 = Top
            and self.segment_stripes[1].is_off(self.bg_colors, self.fg_colors) # 1 = Top Right
            and self.segment_stripes[2].is_on(self.bg_colors, self.fg_colors) # 2 = Bottom Right
            and self.segment_stripes[3].is_on(self.bg_colors, self.fg_colors) # 3 = Bottom
            and self.segment_stripes[4].is_on(self.bg_colors, self.fg_colors) # 4 = Bottom Left
            and self.segment_stripes[5].is_on(self.bg_colors, self.fg_colors) # 5 = Top Left
            and self.segment_stripes[6].is_on(self.bg_colors, self.fg_colors) # 6 = Middle
        )

    def _is_7(self):
        return (
            self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors) # 0 = Top
            and self.segment_stripes[1].is_on(self.bg_colors, self.fg_colors) # 1 = Top Right
            and self.segment_stripes[2].is_on(self.bg_colors, self.fg_colors) # 2 = Bottom Right
            and self.segment_stripes[3].is_off(self.bg_colors, self.fg_colors) # 3 = Bottom
            and self.segment_stripes[4].is_off(self.bg_colors, self.fg_colors) # 4 = Bottom Left
            and self.segment_stripes[5].is_off(self.bg_colors, self.fg_colors) # 5 = Top Left
            and self.segment_stripes[6].is_off(self.bg_colors, self.fg_colors) # 6 = Middle
        )

    def _is_8(self):
        return (
            self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors) # 0 = Top
            and self.segment_stripes[1].is_on(self.bg_colors, self.fg_colors) # 1 = Top Right
            and self.segment_stripes[2].is_on(self.bg_colors, self.fg_colors) # 2 = Bottom Right
            and self.segment_stripes[3].is_on(self.bg_colors, self.fg_colors) # 3 = Bottom
            and self.segment_stripes[4].is_on(self.bg_colors, self.fg_colors) # 4 = Bottom Left
            and self.segment_stripes[5].is_on(self.bg_colors, self.fg_colors) # 5 = Top Left
            and self.segment_stripes[6].is_on(self.bg_colors, self.fg_colors) # 6 = Middle
        )

    def _is_9(self):
        return (
            self.segment_stripes[0].is_on(self.bg_colors, self.fg_colors) # 0 = Top
            and self.segment_stripes[1].is_on(self.bg_colors, self.fg_colors) # 1 = Top Right
            and self.segment_stripes[2].is_on(self.bg_colors, self.fg_colors) # 2 = Bottom Right
            and self.segment_stripes[3].is_on(self.bg_colors, self.fg_colors) # 3 = Bottom
            and self.segment_stripes[4].is_off(self.bg_colors, self.fg_colors) # 4 = Bottom Left
            and self.segment_stripes[5].is_on(self.bg_colors, self.fg_colors) # 5 = Top Left
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