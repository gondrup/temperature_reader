#!/usr/bin/env python

from tempocr import imageprocess

#image_file = "test_images/auto_2018-01-25_154141.jpg"
image_file = "test_images/auto_2018-01-25_165521.jpg"

im = imageprocess.prepare_for_ocr(image_file)