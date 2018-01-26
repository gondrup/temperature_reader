from tempocr.color import compare

# Imported these for testing/debugging only, remove later!
from PIL import Image, ImageDraw
from pprint import pprint

import sys

MARKER_COLOR = [255, 158, 141]

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

def find_clusters_from_pixel_matrix(pixel_matrix):
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

def find_screen(im):
    rgb_im = im.convert('RGB')

    #draw = ImageDraw.Draw(rgb_im)

    w = rgb_im.size[0]
    h = rgb_im.size[1]

    marker_pixel_matrix = [[False for x in range(w)] for y in range(h)] 

    # 1. Find pixels that contain colours similar to expected marker colour

    for i in range(h):
        for j in range(w):
            #row = [rgb_im.getpixel((j,i)) ]
            pixel = rgb_im.getpixel((j, i))

            if(compare.is_similar(pixel, MARKER_COLOR, compare.SIMILARITY_THRESHOLD)):
                #print "Match!", j, i, pixel
                #draw.point((j, i), fill="lightgreen")
                marker_pixel_matrix[i][j] = True

    #rgb_im.save(sys.stdout, "PNG")

    # 2. Determine pixel clusters

    clusters = find_clusters_from_pixel_matrix(marker_pixel_matrix)

    # Include only the 4 largest clusters, these should be the corners
    clusters.sort(lambda x,y: cmp(len(y), len(x)))
    clusters = clusters[:4]

    #print len(clusters)

    #for index, cluster in enumerate(clusters):

    #draw = ImageDraw.Draw(rgb_im)
    #for cluster in clusters:
    #    for x, y in cluster:
    #        draw.point((x, y), fill="lightgreen")
    #
    #rgb_im.save(sys.stdout, "PNG")

    # 3. Create Marker objects for each cluster (total 4)

    markers = []
    for cluster in clusters:
        markers.append(cluster_to_marker(cluster))

    # 4. Determine which clusters represent which corner

    markerTL = None
    markerTR = None
    markerBR = None
    markerBL = None

    markers.sort(lambda x,y: cmp(x.point_tl[0], y.point_tl[0]))
    markers.sort(lambda x,y: cmp(x.point_tl[1], y.point_tl[1]))
    
    markerTL = markers[0]
    markerTR = markers[1]

    markers.sort(lambda x,y: cmp(y.point_tl[1], x.point_tl[1]))
    markers.sort(lambda x,y: cmp(x.point_tl[0], y.point_tl[0]))

    markerBL = markers[0]
    markerBR = markers[1]

    # 5. Create and return a Screen object with these markers

    screen = Screen(markerTL, markerTR, markerBL, markerBR)

    print 'TL', markerTL.point_tl, markerTL.point_br
    print 'TR', markerTR.point_tl, markerTR.point_br
    print 'BL', markerBL.point_tl, markerBL.point_br
    print 'BR', markerBR.point_tl, markerBR.point_br




def cluster_to_marker(cluster):
    cluster.sort(lambda x,y: cmp(x[1], y[1]))
    cluster.sort(lambda x,y: cmp(x[0], y[0]))

    return Marker(cluster[0], cluster[-1])
