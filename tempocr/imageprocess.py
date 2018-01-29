from PIL import Image
import subprocess
import sys
from tempocr import screen

def get_coords_str_from_screen(screen, image_width, image_height, offsets = None):
    coords_str = ''

    coords_str += '%d,%d,%d,%d' % (screen.markerTL.point_br[0], screen.markerTL.point_br[1], 0, 0)
    coords_str += ' %d,%d,%d,%d' % (screen.markerTR.point_tl[0], screen.markerTR.point_br[1], image_width, 0)
    coords_str += ' %d,%d,%d,%d' % (screen.markerBL.point_br[0], screen.markerBL.point_tl[1], 0, image_height)
    coords_str += ' %d,%d,%d,%d' % (screen.markerBR.point_tl[0], screen.markerBR.point_tl[1], image_width, image_height)
    
    return coords_str

def fix_perspective(image_file):
    # 1. Load image

    im = Image.open(image_file)
    width, height = im.size

    # 2. Use screen module to find the screen

    found_screen = screen.find_screen(im)

    # 3. Use the found screen object to fix the perspective and crop the image

    coords_str = get_coords_str_from_screen(found_screen, width, height)

    #print 'Cropping %dx%d image with coords: %s' % (width, height, coords_str)

    cmd = [
        "convert", image_file, "-matte", "-virtual-pixel", "transparent",
        "-distort", "Perspective", coords_str,
        "-resize", "640x480!",
        "txt:"
    ]

    output_stream = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    return output_stream

    # Find coords

    #proc = subprocess.Popen(["convert", image_file, "txt:"],stdout=subprocess.PIPE)
    #while True:
    #    line = proc.stdout.readline()
    #    if line != '':
    #        #the real code does filtering here
    #        print "test:", line.rstrip()
    #    else:
    #        break
    #
    #return im

    #coords = [
    #    [(645,1632), (0,0)],
    #    [(743,2941), (0,height)],
    #    [(2600,2993), (width,height)],
    #    [(2592,1494), (width,0)],
    #]

    # Run the perspective fix with IM

    #coords_str = ""
    #for point_from, point_to in coords:
    #    coords_str += str(point_from[0]) + "," + str(point_from[1])
    #    coords_str += " " + str(point_to[0]) + "," + str(point_to[1]) + " "

    #print "Coords: " + coords_str

    # First attempt, didn't work, way too complicated
    '''
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
    '''

def prepare_for_ocr(image_file):
    return fix_perspective(image_file)