import unittest
import sys

from PIL import Image

sys.path.append('../')
from tempocr import screen
from tempocr import imageprocess

class TestImageProcess(unittest.TestCase):
    def test_get_coords_str_from_screen(self):
        # Original test with made up coords

        markerTL = screen.Marker((1, 1), (5, 5))
        markerTR = screen.Marker((101, 1), (105, 5))
        markerBL = screen.Marker((1, 101), (5, 105))
        markerBR = screen.Marker((101, 101), (105, 105))

        w = 640
        h = 480

        test_screen = screen.Screen(markerTL, markerTR, markerBL, markerBR)

        coords_str = imageprocess.get_coords_str_from_screen(test_screen, w, h)

        expected = '5,5,0,0 101,5,640,0 5,101,0,480 101,101,640,480'
        assert coords_str == expected, 'Coords string didn\'t match, expected: %s got: %s' % (expected, coords_str)

        # New test based on fixture image

        markerTL = screen.Marker((1, 8), (12, 13))
        markerTR = screen.Marker((38, 8), (40, 12))
        markerBL = screen.Marker((13, 35), (17, 38))
        markerBR = screen.Marker((40, 38), (45, 43))

        w = 50
        h = 50

        test_screen = screen.Screen(markerTL, markerTR, markerBL, markerBR)

        coords_str = imageprocess.get_coords_str_from_screen(test_screen, w, h)

        expected = '12,13,0,0 38,12,50,0 17,35,0,50 40,38,50,50'
        assert coords_str == expected, 'Coords string didn\'t match, expected: %s got: %s' % (expected, coords_str)

    def test_fix_perspective(self):
        image_file = "tests/fixtures/markers_with_box.gif"
        im = Image.open(image_file)

        fixed_image = imageprocess.fix_perspective(image_file)

        #file = open('tests/fixtures/out.png', 'w')
        #file.write(fixed_image)
        #file.close()

        assert fixed_image != None

if __name__ == '__main__':
    unittest.main()
