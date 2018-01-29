import unittest
import sys

from PIL import Image

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


    def pixel_active_in_fixture(self, x, y):
        active_pixels = [
            (9, 8), (10, 8), (11, 8), (38, 8), (39, 8), (40, 8),
            (8, 9), (9, 9), (10, 9), (11, 9), (12, 9), (38, 9), (39, 9), (40, 9),
            (8, 10), (9, 10), (10, 10), (11, 10), (12, 10), (38, 10), (39, 10), (40, 10),
            (9, 11), (10, 11), (11, 11), (12, 11), (38, 11), (39, 11), (40, 11),
            (10, 12), (11, 12), (12, 12), (40, 12),
            (11, 13), (12, 13),
            (24, 28),
            (14, 35), (15, 35), (16, 35), (17, 35),
            (13, 36), (14, 36), (15, 36), (16, 36), (17, 36),
            (13, 37), (14, 37), (15, 37), (16, 37), (17, 37),
            (13, 38), (14, 38), (15, 38), (16, 38), (40, 38), (41, 38), (42, 38), (43, 38),
            (40, 39), (41, 39), (42, 39), (43, 39), (44, 39),
            (40, 40), (41, 40), (42, 40), (43, 40), (44, 40), (45, 40),
            (40, 41), (41, 41), (42, 41), (43, 41), (44, 41), (45, 41),
            (40, 42), (41, 42), (42, 42), (43, 42), (44, 42), (45, 42),
            (42, 43), (43, 43), (44, 43)
        ]

        for pixel in active_pixels:
            if pixel[0] == x and pixel[1] == y:
                return True

        return False

    def test_get_marker_pixel_matrix_from_image(self):
        image_file = "tests/fixtures/markers.gif"
        im = Image.open(image_file)

        marker_matrix = screen.get_marker_pixel_matrix_from_image(im)

        for y, row in enumerate(marker_matrix):
            for x, col in enumerate(row):
                if self.pixel_active_in_fixture(x, y):
                    assert col == True, "Active pixel expected at %d, %d" % (x, y)
                else:
                    assert col == False, "Inactive pixel expected at %d, %d" % (x, y)

    def test_get_markers_from_clusters(self):
        clusters = [
            [(1, 1),(1, 2),(1, 3),(1, 4),(5, 5)],
            [(101, 1),(101, 2),(101, 3),(101, 4),(105, 5)],
            [(1, 101),(1, 102),(1, 103),(1, 104),(5, 105)],
            [(101, 101),(101, 102),(101, 103),(101, 104),(105, 105)],
            [(51, 51),(51, 52)]
        ]

        markers = screen.get_markers_from_clusters(clusters)

        assert len(markers) == 4

    def test_create_screen_from_markers(self):
        pointTL = (1, 1), (5, 5)
        pointTR = (101, 1), (105, 5)
        pointBL = (1, 101), (5, 105)
        pointBR = (101, 101), (105, 105)

        markers = [
            screen.Marker(pointTR[0], pointTR[1]),
            screen.Marker(pointTL[0], pointTL[1]),
            screen.Marker(pointBR[0], pointBR[1]),
            screen.Marker(pointBL[0], pointBL[1]),
        ]

        created_screen = screen.create_screen_from_markers(markers)

        assert created_screen.markerTL.point_tl == pointTL[0], "Top left point wrong, expected: %s - got: %s" % (pointTL[0], created_screen.markerTL.point_tl)
        assert created_screen.markerTR.point_tl == pointTR[0], "Top right point wrong, expected: %s - got: %s" % (pointTR[0], created_screen.markerTR.point_tl)
        assert created_screen.markerBL.point_tl == pointBL[0], "Bottom left point wrong, expected: %s - got: %s" % (pointBL[0], created_screen.markerBL.point_tl)
        assert created_screen.markerBR.point_tl == pointBR[0], "Bottom right point wrong, expected: %s - got: %s" % (pointBR[0], created_screen.markerBR.point_tl)

        pointTL = (1, 8), (12, 13)
        pointTR = (38, 8), (40, 12)
        pointBL = (13, 35), (17, 38)
        pointBR = (40, 38), (45, 43)

        markers = [
            screen.Marker(pointTL[0], pointTL[1]),
            screen.Marker(pointTR[0], pointTR[1]),
            screen.Marker(pointBL[0], pointBL[1]),
            screen.Marker(pointBR[0], pointBR[1]),
        ]

        created_screen = screen.create_screen_from_markers(markers)

        assert created_screen.markerTL.point_tl == pointTL[0], "Top left point wrong, expected: %s - got: %s" % (pointTL[0], created_screen.markerTL.point_tl)
        assert created_screen.markerTR.point_tl == pointTR[0], "Top right point wrong, expected: %s - got: %s" % (pointTR[0], created_screen.markerTR.point_tl)
        assert created_screen.markerBL.point_tl == pointBL[0], "Bottom left point wrong, expected: %s - got: %s" % (pointBL[0], created_screen.markerBL.point_tl)
        assert created_screen.markerBR.point_tl == pointBR[0], "Bottom right point wrong, expected: %s - got: %s" % (pointBR[0], created_screen.markerBR.point_tl)

if __name__ == '__main__':
    unittest.main()