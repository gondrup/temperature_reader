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

    def test_in_clusters(self):
        clusters = [
            [
                (1, 1),
                (1, 2),
                (1, 3),
                (1, 4),
                (5, 5)
            ]
        ]

        assert screen.in_clusters(0, 0, clusters) == False
        assert screen.in_clusters(1, 1, clusters) == True
        assert screen.in_clusters(1, 2, clusters) == True
        assert screen.in_clusters(1, 3, clusters) == True
        assert screen.in_clusters(1, 4, clusters) == True
        assert screen.in_clusters(1, 5, clusters) == False
        assert screen.in_clusters(2, 5, clusters) == False
        assert screen.in_clusters(5, 5, clusters) == True

    def test_get_cluster_from_pixel_matrix_at_loc(self):
    	pixel_matrix = [
    		[False, False, False, False, False],
    		[False, True, False, False, False],
    		[False, True, True, False, False],
    		[False, False, False, False, False],
    		[False, False, False, False, False],
    	]

    	cluster = screen.get_cluster_from_pixel_matrix_at_loc(pixel_matrix, 1, 2)
    	assert len(cluster) == 3

        cluster = screen.get_cluster_from_pixel_matrix_at_loc(pixel_matrix, 2, 2)
        assert len(cluster) == 3

        cluster = screen.get_cluster_from_pixel_matrix_at_loc(pixel_matrix, 2, 3)
        assert len(cluster) == 3

        cluster = screen.get_cluster_from_pixel_matrix_at_loc(pixel_matrix, 4, 4)
        assert len(cluster) == 0

        cluster = screen.get_cluster_from_pixel_matrix_at_loc(pixel_matrix, 0, 2)
        assert len(cluster) == 0

    def test_add_cluster_from_pixel_matrix_at_loc(self):
        pixel_matrix = [
            [False, False, False, False, False],
            [False, True, False, False, False],
            [False, True, True, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
        ]
        clusters = []
        clusters = screen.add_cluster_from_pixel_matrix_at_loc(clusters, pixel_matrix, 1, 2)
        assert len(clusters) == 1

        clusters = [
            [(0, 0)]
        ]
        clusters = screen.add_cluster_from_pixel_matrix_at_loc(clusters, pixel_matrix, 1, 2)
        assert len(clusters) == 2
        assert clusters[0] == [(0, 0)]
        assert clusters[1] == [(1, 1), (1, 2), (2, 2)]

        clusters = []
        clusters = screen.add_cluster_from_pixel_matrix_at_loc(clusters, pixel_matrix, 4, 4)
        assert len(clusters) == 0

    def test_find_clusters_in_pixel_matrix(self):
        pixel_matrix = [
            [False, False, False, False, False],
            [False, True, False, False, False],
            [False, True, True, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
        ]

        clusters = screen.find_clusters_in_pixel_matrix(pixel_matrix)
        assert len(clusters) == 1

    def test_cluster_to_marker(self):
        cluster = [(1, 1), (1, 2), (2, 2)]

        marker = screen.cluster_to_marker(cluster)

        self.assertIsNotNone(marker)
        self.assertIsInstance(marker, screen.Marker)

        assert marker.point_tl == (1, 1)
        assert marker.point_br == (2, 2)

if __name__ == '__main__':
    unittest.main()