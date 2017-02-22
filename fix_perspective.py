#!/usr/bin/env python

from tempocr import imageprocess

image_file = "test_images/20170209_135025.jpg"

im = imageprocess.prepare_for_ocr(image_file)