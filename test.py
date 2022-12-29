import cv2
import os
import numpy as np
import mouse
import pyautogui
from random import randint, shuffle
from natsort import natsorted

directory = 'SRC/tiles'

# backg = cv2.imread('SRC/dest.png')
# # backg = cv2.cvtColor(backg, cv2.COLOR_BGR2RGB)
# tile = cv2.imread('SRC/tiles/9.png')
# # tile = cv2.cvtColor(tile, cv2.COLOR_BGR2RGB)

color_edge = [180, 175, 150]
color_face = [233, 229, 212]
#


tile_list = natsorted(os.listdir(directory))

# result = cv2.VideoWriter('test.avi', cv2.VideoWriter_fourcc(*'DIVX'), 20, (1920, 1080))

folder_counter = -1

while True:
    title = -1
    backg = pyautogui.screenshot()
    backg = np.array(backg)
    backg = cv2.cvtColor(backg, cv2.COLOR_RGB2BGR)

    # result.write(backg)
    # cv2.imshow('Test', backg)

    circles = []
    flowers = []

    for file in tile_list:

        folder_counter += 1
        title += 1
        path = os.path.join(directory, file)
        tile = cv2.imread(path)
        tile = cv2.cvtColor(tile, cv2.COLOR_BGR2RGB)

        w = tile.shape[1]
        h = tile.shape[0]

        tl, br = (0, 0)

        output = cv2.matchTemplate(backg, tile, cv2.TM_SQDIFF_NORMED)

        # if title == 46 or title == 28:
        #     thresh = 0.70
        # elif title == 35:
        #     thresh = 0.63
        # elif title == 33:
        #     thresh = 0.60
        # else:
        #     thresh = 0.79

        if title == 26:
            thresh = 0.020
        elif title == 36:
            thresh = 0.030
        elif title == 31 or title == 27:
            thresh = 0.040
        elif title == 28:
            thresh = 0.050
        elif title == 32 or title == 0 or title == 6 or title == 16:
            thresh = 0.060
        elif title == 38 or title == 39:
            thresh = 0.070
        elif title == 33:
            thresh = 0.080
        elif title == 34 or title == 40:
            thresh = 0.085
        elif title == 25:
            thresh = 0.090
        elif title == 24:
            thresh = 0.117
        elif title == 7:
            thresh = 0.120
        elif title == 5 or title == 33:
            thresh = 0.140
        elif title == 18 or title == 8:
            thresh = 0.000
        else:
            thresh = 0.045
        loc = np.where(output <= thresh)
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
            if (cur_x - 10 < fut_x < cur_x + 10) or (cur_y - 10 < fut_y < cur_y + 10):
                loc.pop(i + 1)
            else:
                i += 1
        i = 0
        while i != len(flowers) - 1 and len(flowers) != 0:
            f_cur_x, f_cur_y = flowers[i]
            f_fut_x, f_fut_y = flowers[i + 1]

            if (f_cur_x - 10 < f_fut_x < f_cur_x + 10) or (f_cur_y - 10 < f_fut_y < f_cur_y + 10):
                flowers.pop(i + 1)
            else:
                i += 1
        i = 0
        while i != len(circles) - 1 and len(circles) != 0:
            c_cur_x, c_cur_y = circles[i]
            c_fut_x, c_fut_y = circles[i + 1]

            if (c_cur_x - 10 < c_fut_x < c_cur_x + 10) or (c_cur_y - 10 < c_fut_y < c_cur_y + 10):
                circles.pop(i + 1)
            else:
                i += 1

        # delete obvious miscolored estimates
        j = 0
        height, width, chan = tile.shape
        color_to_match = [230, 224, 203]


        # print(loc)
        bad_tiles = []

        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)

        for pt in loc:
            tl = pt
            br = (tl[0]+w, tl[1]+h)

            pt_color = backg[tl[1], tl[0]]
            pt_color = pt_color[::-1]

            # print(tl)
            # print(pt_color)

            color_match = 0
            for i in range(len(pt_color)):
                # if (pt_color[i] < 1.03 * color_edge[i] and pt_color[i] > .96 * color_edge[i]) or
                # (pt_color[i] < 1.03 * color_face[i] and pt_color[i] > .80 * color_face[i]):
                if True:
                    color_match += 1

            if color_match == 3:
                # print(color_match)
                cv2.circle(backg, (tl[0], tl[1]), 5, (255, 0, 0), -1)
                # mouse.move(tl[0]+150, tl[1]+70, True, 0.2)

            # append to list of tiles to delete
            if color_match != 3:
                bad_tiles.append((tl[0], tl[1]))

            # append circle or flower coordinates
            if 0 < title < 5:
                circles.append((tl[0], tl[1]))
            if 4 < title < 9:
                flowers.append((tl[0], tl[1]))

            cv2.rectangle(backg, tl, br, (r, g, b), 2)

            # cv2.imshow('title', backg)
            # cv2.waitKey()

        if folder_counter <= 41:
            cv2.imwrite('forloop/' + str(title) + '.jpg', backg)
        # print(bad_tiles)

        i = 0
        count = 0
        deleted = 0
        total = len(loc)

        # delete inactive tiles after ID from list of 'to press' candidates
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

        shuffle(loc)
        # move and press only if two active tiles (unique)
        flower = 0
        if len(flowers) > 1:
            while len(flowers) > 1:
                pt_x, pt_y = flowers[flower]
                mouse.move(pt_x + 25, pt_y + 25, True, 0.01)
                mouse.click()
                flower += 1
                if flower == 2:
                    flowers.pop(1)
                    flowers.pop(0)
                    flower = 0

        circle = 0
        if len(circles) > 1:
            while len(circles) > 1:
                pt_x, pt_y = circles[circle]
                mouse.move(pt_x + 25, pt_y + 25, True, 0.01)
                mouse.click()
                circle += 1
                if circle == 2:
                    circles.pop(1)
                    circles.pop(0)
                    circle = 0

        # move and press only if two active tiles (non-unique)
        k = 0
        if len(loc) % 2 == 0:
            for tile in loc:
                mouse.move(tile[0]+25, tile[1]+25, True, 0.01)
                mouse.click()

        elif len(loc) >= 3 and len(loc) % 2 == 1:
            while k != len(loc) - 1:
                pt = loc[k]
                mouse.move(pt[0]+25, pt[1]+25, True, 0.01)
                mouse.click()
                k += 1

    if cv2.waitKey(1) and 0xFF == 27:
        break

# result.release()

cv2.destroyAllWindows()

#
# cv2.imshow('title', backg)
# cv2.waitKey()
