from tempocr.color import compare

# Imported these for testing/debugging only, remove later!
#from PIL import Image, ImageDraw
import sys

MARKER_COLOR = [255, 158, 141]

def in_cluster(x, y, cluster):
    for check_x, check_y in cluster:
        if (check_x == x and check_y == y):
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

    print 'xy:', x, y, 'wh:', w, h

    to_check = []

    if (x > 0):
        # Row 1
        if (y > 0):
            to_check.append((x-1, y-1))
            to_check.append((x, y-1))
            if (x < w):
                to_check.append((x+1, y-1))

        # Row 2
        to_check.append((x-1, y))
        if (x < w):
            to_check.append((x+1, y))

        # Row 3
        if (y < h):
            to_check.append((x-1, y+1))
            to_check.append((x, y+1))

            if (x < w):
                to_check.append((x+1, y+1))

    for check_x, check_y in to_check:
        if in_cluster(check_x, check_y, cluster) == False and pixel_matrix[check_x][check_y] == True:
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

    for y, row in enumerate(pixel_matrix, 0):
        for x, value in enumerate(row, 0):
            if (value == True):
                if len(clusters) > 0:
                    for check_cluster in clusters:
                        if in_cluster(x, y, check_cluster) == False:
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

    print len(clusters)

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
