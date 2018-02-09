from PIL import Image
import subprocess
from subprocess import call
import sys
import tempfile
from tempocr import screen

def get_coords_str_from_screen(screen, image_width, image_height, offsets = None):
    coords_str = ''

    coords_str += '%d,%d,%d,%d' % (screen.markerTL.point_br[0], screen.markerTL.point_br[1], 0, 0)
    coords_str += ' %d,%d,%d,%d' % (screen.markerTR.point_tl[0], screen.markerTR.point_br[1], image_width, 0)
    coords_str += ' %d,%d,%d,%d' % (screen.markerBL.point_br[0], screen.markerBL.point_tl[1], 0, image_height)
    coords_str += ' %d,%d,%d,%d' % (screen.markerBR.point_tl[0], screen.markerBR.point_tl[1], image_width, image_height)
    
    return coords_str

def fix_perspective(image_file, marker_color):
    # 1. Load image
    im = Image.open(image_file)
    
    # Resize image down for performance improvement
    im = im.resize((160, 120), resample=Image.NEAREST)
    
    width, height = im.size

    # 2. Use screen module to find the screen
    found_screen = screen.find_screen(im, marker_color)

    # 3. Use the found screen object to fix the perspective and crop the image
    coords_str = get_coords_str_from_screen(found_screen, width, height)

    #print 'Cropping %dx%d image with coords: %s' % (width, height, coords_str)

    temp_file = tempfile.NamedTemporaryFile()
    im.save(temp_file.name, 'PNG')

    # TODO: Use input image resolution as output resolution below
    cmd = [
        'convert', temp_file.name, '-matte', '-virtual-pixel', 'transparent',
        '-distort', 'Perspective', coords_str,
        'png:{}'.format(temp_file.name)
    ]

    call(cmd)

    return temp_file

def prepare_for_ocr(image_file, marker_color):
    return fix_perspective(image_file, marker_color)
