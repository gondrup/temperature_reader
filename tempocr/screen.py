from tempocr.color import compare
import sys

#MARKER_COLOR = [255, 158, 141]
#MARKER_COLOR = [255, 100, 60]

class Marker:
    def __init__(self, point_tl, point_br):
        self.point_tl = point_tl
        self.point_br = point_br

    def is_above(self, marker):
        return self.point_tl[1] > marker.point_tl[1]

    def is_left_of(self, marker):
        return self.point_tl[0] < marker.point_tl[0]

class Screen:
    def __init__(self, markerTL, markerTR, markerBL, markerBR):
        self.markerTL = markerTL
        self.markerTR = markerTR
        self.markerBL = markerBL
        self.markerBR = markerBR

def in_cluster(x, y, cluster):
    for check_x, check_y in cluster:
        if (check_x == x and check_y == y):
            return True

    return False

def in_clusters(x, y, clusters):
    for check_cluster in clusters:
        if in_cluster(x, y, check_cluster) == True:
            return True

    return False

def get_cluster_from_pixel_matrix_at_loc(pixel_matrix, x, y, cluster = None):
    #
    #   1 2 3
    #   4 # 5
    #   6 7 8
    #

    if cluster is None:
        cluster = []

    h = len(pixel_matrix)

    if (h > 0):
        w = len(pixel_matrix[0])
    else:
        w = 0

    max_x = w - 1
    max_y = h - 1

    to_check = []

    if (x > 0):
        # Row 1
        if (y > 0):
            to_check.append((x-1, y-1))
            to_check.append((x, y-1))
            if (x < max_x):
                to_check.append((x+1, y-1))

        # Row 2
        to_check.append((x-1, y))
        if (x < max_x):
            to_check.append((x+1, y))

        # Row 3
        if (y < max_y):
            to_check.append((x-1, y+1))
            to_check.append((x, y+1))

            if (x < max_x):
                to_check.append((x+1, y+1))

    for check_x, check_y in to_check:
        if in_cluster(check_x, check_y, cluster) == False and pixel_matrix[check_y][check_x] == True:
            cluster.append((check_x, check_y))
            cluster = get_cluster_from_pixel_matrix_at_loc(pixel_matrix, check_x, check_y, cluster)

    return cluster

def add_cluster_from_pixel_matrix_at_loc(clusters, pixel_matrix, x, y):
    cluster = get_cluster_from_pixel_matrix_at_loc(pixel_matrix, x, y)
    if (len(cluster) > 1):
        clusters.append(cluster)

    return clusters

def find_clusters_in_pixel_matrix(pixel_matrix):
    clusters = []

    for y, row in enumerate(pixel_matrix):
        for x, value in enumerate(row):
            if (value == True):
                if len(clusters) > 0:
                    if in_clusters(x, y, clusters) == False:
                        clusters = add_cluster_from_pixel_matrix_at_loc(clusters, pixel_matrix, x, y)
                else:
                    clusters = add_cluster_from_pixel_matrix_at_loc(clusters, pixel_matrix, x, y)



    return clusters

def cluster_to_marker(cluster):
    cluster.sort(key=lambda x: x[1])
    cluster.sort(key=lambda x: x[0])

    return Marker(cluster[0], cluster[-1])

def get_marker_pixel_matrix_from_image(im, marker_color):
    rgb_im = im.convert('RGB')

    w = rgb_im.size[0]
    h = rgb_im.size[1]

    marker_pixel_matrix = [[False for x in range(w)] for y in range(h)] 

    for i in range(h):
        for j in range(w):
            pixel = rgb_im.getpixel((j, i))

            if(compare.is_similar(pixel, marker_color, compare.SIMILARITY_THRESHOLD)):
                marker_pixel_matrix[i][j] = True

    return marker_pixel_matrix

def get_markers_from_clusters(clusters):
    # Include only the 4 largest clusters, these should be the corners
    clusters.sort(key=lambda x: len(x))
    clusters = clusters[:4]

    markers = []
    for cluster in clusters:
        markers.append(cluster_to_marker(cluster))

    return markers

def create_screen_from_markers(markers):
    if len(markers) != 4:
        raise ValueError('Expected 4 screen marker points, got %d' % (len(markers)))

    markerTL = None
    markerTR = None
    markerBR = None
    markerBL = None

    # Top/Bottom
    markers.sort(key=lambda x: x.point_br[1])
    top_markers = [markers[0], markers[1]]
    bottom_markers = [markers[2], markers[3]]

    # Left/Right
    if top_markers[0].point_br[0] >= top_markers[1].point_br[0]:
        markerTL = top_markers[1]
        markerTR = top_markers[0]
    else:
        markerTL = top_markers[0]
        markerTR = top_markers[1]

    if bottom_markers[0].point_tl[0] >= bottom_markers[1].point_tl[0]:
        markerBL = bottom_markers[1]
        markerBR = bottom_markers[0]
    else:
        markerBL = bottom_markers[0]
        markerBR = bottom_markers[1]

    screen = Screen(markerTL, markerTR, markerBL, markerBR)

    return screen

def find_screen(im, marker_color):
    # 1. Find pixels that contain colours similar to expected marker colour
    marker_pixel_matrix = get_marker_pixel_matrix_from_image(im, marker_color)

    # 2. Determine pixel clusters
    clusters = find_clusters_in_pixel_matrix(marker_pixel_matrix)

    # 3. Create Marker objects for each cluster (total 4)
    markers = get_markers_from_clusters(clusters)

    # 4. Create and return a Screen object with these markers
    return create_screen_from_markers(markers)
