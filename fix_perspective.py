#!/usr/bin/env python

from PIL import Image
import sys
import numpy

def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

im = Image.open("test_images/20170209_135025.jpg")
width, height = im.size

coeffs = find_coeffs(
        [(671, 1638), (2592, 1494), (743, 2941), (2600, 2993)],
        [(0, 0), (width, 0), (width, height), (0, height)])

im.transform((width, height), Image.PERSPECTIVE, coeffs,
        Image.BICUBIC)

im.save(sys.stdout, "PNG")