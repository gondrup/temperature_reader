#!/usr/bin/env python

from os import path
from tempocr import imageprocess

#image_file = 'test_images/auto_2018-01-29_141232.jpg'
#image_file = 'test_images/auto_2018-02-06_135534.jpg'
image_file = 'test_images/20180206_153314_scaled_down.jpg'
#image_file = 'tests/fixtures/markers_with_box.gif'
output_file = '{}/{}_fixed.png'.format(path.dirname(image_file), path.splitext(path.basename(image_file))[0]);

print 'Fix Perspective'
print '---------------'
print 'Input file: {} \nOutput file: {}'.format(image_file, output_file)
print ''

tmp = imageprocess.prepare_for_ocr(image_file)

new_image_file = open(output_file, 'w')
new_image_file.write(tmp.read())
tmp.close()
new_image_file.close()