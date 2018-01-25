# Similarity formula taken from http://stackoverflow.com/a/26768008
#
#SIMILARITY_THRESHOLD = 5
#
#def luminance(pixel):
#    return (0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])
#
#def get_difference(pixel_a, pixel_b):
#    return abs(luminance(pixel_a) - luminance(pixel_b))
#
#def is_similar(pixel_a, pixel_b, threshold):
#    return get_difference(pixel_a, pixel_b) < threshold

# 
# http://hanzratech.in/2015/01/16/color-difference-between-2-colors-using-python.html

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

SIMILARITY_THRESHOLD = 5

def get_difference(pixel_a, pixel_b):
	color1_rgb = sRGBColor((pixel_a[0]/255.0), (pixel_a[1]/255.0), (pixel_a[2]/255.0));
	color2_rgb = sRGBColor((pixel_b[0]/255.0), (pixel_b[1]/255.0), (pixel_b[2]/255.0));

	color1_lab = convert_color(color1_rgb, LabColor);
	color2_lab = convert_color(color2_rgb, LabColor);

	delta_e = delta_e_cie2000(color1_lab, color2_lab);

	return delta_e

def is_similar(pixel_a, pixel_b, threshold):
    return get_difference(pixel_a, pixel_b) < threshold