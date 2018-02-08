#!/usr/bin/env python

from PIL import Image
from tempocr.digit_recognition import read_temperature

image_file = 'test_images/auto_2018-01-29_141232_fixed.png'
#image_file = 'test_images/20180206_153314_scaled_down_fixed.png'

print('Read Temperature')
print('----------------')
print('Input file: {}'.format(image_file))
print('')

im = Image.open(image_file)
temperature = read_temperature(im)

print('Temperature: {}'.format(temperature))

#307200
#12192768