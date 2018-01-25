from tempocr.color import compare

# Imported these for testing/debugging only, remove later!
from PIL import Image, ImageDraw
import sys


MARKER_COLOR = [255, 158, 141]

def find_screen(im):
    rgb_im = im.convert('RGB')

    draw = ImageDraw.Draw(rgb_im)

    # 1. Find pixels that contain colours similar to expected marker colour

    for i in range(rgb_im.size[1]):
        for j in range(rgb_im.size[0]):
            #row = [rgb_im.getpixel((j,i)) ]
            pixel = rgb_im.getpixel((j, i))

            if(compare.is_similar(pixel, MARKER_COLOR, compare.SIMILARITY_THRESHOLD)):
                #print "Match!", j, i, pixel
                draw.point((j, i), fill="lightgreen")

    rgb_im.save(sys.stdout, "PNG")

    # 2. Determine pixel clusters
    # 3. Determine which clusters represent which corner
    # 4. Create Marker objects for each cluster (total 4)
    # 5. Create and return a Screen object with these markers


class Marker:
    COORD_HIGHEST = "H"
    COORD_LOWEST = "L"

    def __init__(self, coords):
        self.coords = coords

    def get_coords(x_hl, y_hl):
        found_x = 0
        found_y = 0

#        for x, y in coords:
 #           if(x_hl = self.COORD_HIGHEST)

    def get_point_tl():
        return 0

class Screen:
    def __init__(self, markerTL, markerTR, markerBR, markerBL):
        self.markerTL = markerTL
        self.markerTR = markerTR
        self.markerBR = markerBR
        self.markerBL = markerBL
