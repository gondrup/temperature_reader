import unittest
import sys

sys.path.append('../')
from tempocr import screen

class TestScreen(unittest.TestCase):
    def test_in_cluster(self):
    	cluster = [
    		(1, 1),
    		(1, 2),
    		(1, 3),
    		(1, 4),
    		(5, 5)
    	]

    	assert screen.in_cluster(0, 0, cluster) == False
        assert screen.in_cluster(1, 1, cluster) == True
        assert screen.in_cluster(1, 2, cluster) == True
        assert screen.in_cluster(1, 3, cluster) == True
        assert screen.in_cluster(1, 4, cluster) == True
        assert screen.in_cluster(1, 5, cluster) == False
        assert screen.in_cluster(2, 5, cluster) == False
        assert screen.in_cluster(5, 5, cluster) == True

    def test_get_cluster_from_pixel_matrix_at_loc(self):
    	pixel_matrix = [
    		[False, False, False, False, False],
    		[False, True, False, False, False],
    		[False, True, True, False, False],
    		[False, False, False, False, False],
    		[False, False, False, False, False],
    	]

    	cluster = screen.get_cluster_from_pixel_matrix_at_loc(pixel_matrix, 1, 2)

    	assert len(cluster) > 0

if __name__ == '__main__':
    unittest.main()