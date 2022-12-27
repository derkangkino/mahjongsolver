import cv2
import os
import numpy as np
import mouse
import pyautogui

directory = 'SRC/tiles'

backg = cv2.imread('SRC/dest4.png')
# # backg = cv2.cvtColor(backg, cv2.COLOR_BGR2RGB)
# tile = cv2.imread('SRC/tiles/9.png')
# # tile = cv2.cvtColor(tile, cv2.COLOR_BGR2RGB)

color_edge = [180, 175, 150]
color_face = [233, 229, 212]
#

title = 0

for file in os.listdir(directory):
    title += 1
    path = os.path.join(directory, file)
    tile = cv2.imread(path)
    tile = cv2.cvtColor(tile, cv2.COLOR_BGR2RGB)

    w = tile.shape[1]
    h = tile.shape[0]

    tl, br = (0, 0)

    output = cv2.matchTemplate(backg, tile, cv2.TM_CCOEFF_NORMED)

    thresh = 0.79
    loc = np.where(output >= thresh)
    # loc looks like this:
    # ([y loc, y loc, y loc]), ([x loc, x loc, x loc])

    # [::-1] reverses list to x,y. *loc removes the redundant layer of array, zip re-arranges so that xy pairs are made
    # instead of being separated
    loc = list(zip(*loc[::-1]))

    # delete extra entries
    i = 0
    while i != len(loc) - 1 and len(loc) != 0:
        cur_x, cur_y = loc[i]
        fut_x, fut_y = loc[i + 1]
        if fut_x > cur_x - 5 and fut_x < cur_x + 5:
            loc.pop(i + 1)
        else:
            i += 1

    # print(loc)
    bad_tiles = []

    for pt in loc:
        tl = pt
        br = (tl[0]+w, tl[1]+h)

        pt_color = backg[tl[1], tl[0]]
        pt_color = pt_color[::-1]

        # print(tl)
        # print(pt_color)

        color_match = 0
        for i in range(len(pt_color)):
            if (pt_color[i] < 1.03 * color_edge[i] and pt_color[i] > .96 * color_edge[i]) or (pt_color[i] < 1.03 * color_face[i] and pt_color[i] > .80 * color_face[i]):

                color_match += 1

        if color_match == 3:
            # print(color_match)
            cv2.circle(backg, (tl[0], tl[1]), 5, (255, 0, 0), -1)
            # mouse.move(tl[0]+150, tl[1]+70, True, 0.2)

        if color_match != 3:
            bad_tiles.append((tl[0], tl[1]))

        cv2.rectangle(backg, tl, br, (0, 0, 255), 2)

        # cv2.imwrite('forloop/'+str(title)+'.jpg', backg)
        cv2.imshow('title', backg)
        cv2.waitKey()

    # print(bad_tiles)

    i = 0
    count = 0
    deleted = 0
    total = len(loc)

    while count != total:
        tile_x, tile_y = loc[i]
        popped = False

        for bad in bad_tiles:

            bad_x = bad[0]
            bad_y = bad[1]

            if deleted != len(bad_tiles):
                if tile_x == bad_x and tile_y == bad_y:
                    loc.pop(i)
                    popped = True
                    deleted += 1

        if popped == False:
            i += 1

        count += 1

    # print('new tile')
    # print(loc)

    k = 0

    if len(loc) % 2 == 0:
        for tile in loc:
            mouse.move(tile[0]+180, tile[1]+70, True, 0.2)
            mouse.click()

    elif len(loc) >= 3 and len(loc) % 2 == 1:
        while k != len(loc) - 1:
            pt = loc[k]
            mouse.move(pt[0]+180, pt[1]+70, True, 0.2)
            mouse.click()
            k += 1



#
# cv2.imshow('title', backg)
# cv2.waitKey()
