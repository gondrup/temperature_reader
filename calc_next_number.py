#!/usr/bin/env python

# First 7 seg digit (2 in pic)
orig = [
    [(634, 80), (636, 170)],
    [(716, 240), (795, 245)],
    [(701, 497), (774, 503)],
    [(594, 573), (592, 661)],
    [(430, 483), (505, 493)],
    [(452, 232), (520, 240)],
    [(615, 325), (615, 413)]
]

new = []

# 411
# 846

for line_coords in orig:
    new.append([
        (line_coords[0][0] + 846, line_coords[0][1]), (line_coords[1][0] + 846, line_coords[1][1])
    ])

print new