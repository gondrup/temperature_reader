#!/usr/bin/env python

from PIL import Image, ImageDraw
from tempocr.digit_recognition import read_temperature
import sys

#image_file = 'test_images/auto_2018-01-29_141232_fixed.png'
image_file = 'test_images/auto_2018-02-06_135534_fixed.png'

print 'Fix Perspective'
print '---------------'
print 'Input file: {}'.format(image_file)
print ''

im = Image.open(image_file)
temperature = read_temperature(im)

print 'Temperature: {}'.format(temperature)