import unittest
import sys

sys.path.append('../')
from tempocr import screen
from tempocr import imageprocess

class TestImageProcess(unittest.TestCase):
    def test_get_coords_str_from_screen(self):
        markerTL = screen.Marker((1, 1), (5, 5))
        markerTR = screen.Marker((101, 1), (105, 5))
        markerBL = screen.Marker((1, 101), (5, 105))
        markerBR = screen.Marker((101, 101), (105, 105))

        w = 640
        h = 480

        test_screen = screen.Screen(markerTL, markerTR, markerBL, markerBR)

        coords_str = imageprocess.get_coords_str_from_screen(test_screen, w, h)

        assert coords_str == '5,5 0,0 101,5 0,640 5,101 0,480 101,101 640,480'

if __name__ == '__main__':
    unittest.main()
