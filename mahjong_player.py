import cv2
import os
import numpy as np
import mouse
import pyautogui
from random import randint, shuffle
from natsort import natsorted

directory = 'SRC/tiles'

tile_list = natsorted(os.listdir(directory))

folder_counter = -1
while_counter = -1


def delete_extra(arr):
    z = 0
    while z != len(arr) - 1 and len(arr) != 0:
        c_cur_x, c_cur_y = arr[z]
        c_fut_x, c_fut_y = arr[z + 1]

        if (c_cur_x - 10 < c_fut_x < c_cur_x + 10) or (c_cur_y - 10 < c_fut_y < c_cur_y + 10):
            arr.pop(z + 1)
        else:
            z += 1


def press(arr):
    z = 0
    if len(arr) > 1:
        while len(arr) > 1:
            ptp_x, ptp_y = arr[z]
            mouse.move(ptp_x + 25, ptp_y + 25, True, 0.01)
            mouse.click()
            z += 1
            if z == 2:
                arr.pop(1)
                arr.pop(0)
                z = 0


while True:

    while_counter += 1

    title = -1

    backg = pyautogui.screenshot()
    backg = np.array(backg)
    backg = cv2.cvtColor(backg, cv2.COLOR_RGB2BGR)

    circles = []
    flowers = []
    gold = []

    for file in tile_list:

        folder_counter += 1
        title += 1
        path = os.path.join(directory, file)
        tile = cv2.imread(path)
        tile = cv2.cvtColor(tile, cv2.COLOR_BGR2RGB)

        w = tile.shape[1]
        h = tile.shape[0]

        tl, br = (0, 0)

        thresholds = [0.060, 0.045, 0.045, 0.045, 0.045, 0.800, 0.060, 0.120, 0.800, 0.045,
                      0.045, 0.045, 0.850, 0.850, 0.900, 0.850, 0.500, 0.800, 0.550, 0.060,
                      0.500, 0.060, 0.045, 0.380, 0.117, 0.500, 0.020, 0.500, 0.050, 0.450,
                      0.045, 0.040, 0.700, 0.500, 0.500, 0.600, 0.030, 0.045, 0.080, 0.500,
                      0.090, 0.075, 0.450, 0.500, 0.900]

        thresh = thresholds[title]

        SQ_CC = [True, True, True, True, True, False, True, True, False, True,
                 True, True, False, False, False, False, False, False, False, True,
                 False, True, True, False, True, False, True, False, True, False,
                 True, True, False, False, False, False, True, True, True, False,
                 True, True, False, False, False]

        SQ = SQ_CC[title]

        if SQ:
            output = cv2.matchTemplate(backg, tile, cv2.TM_SQDIFF_NORMED)
            loc = np.where(output <= thresh)
        else:
            output = cv2.matchTemplate(backg, tile, cv2.TM_CCOEFF_NORMED)
            loc = np.where(output >= thresh)

        loc = list(zip(*loc[::-1]))

        FM = [False, False, False, False, False, False, False, False, False, True,
              True, True, True, True, True, True, True, True, True, True,
              True, True, False, True, False, True, False, False, True, False,
              False, False, False, True, False, True, False, False, False, False,
              False, False, True, False, False]

        delete_extra(loc)
        delete_extra(flowers)
        delete_extra(circles)
        delete_extra(gold)

        i = 0
        color_to_match = [230, 224, 203]
        color_inactive = [197, 193, 176]

        if title == 8 or title == 18 or title == 23 or title == 34 or title == 33 or title == 39 or title == 12:
            while i != len(loc) - 1 and len(loc) != 0:
                tl = loc[i]
                br = (tl[0] + w, tl[1] + h)

                tl_color = backg[tl[1], tl[0]]
                tl_color = tl_color[::-1]
                br_color = backg[br[1], br[0]]
                br_color = br_color[::-1]

                if color_to_match[0] - 25 < tl_color[0] < color_to_match[0] + 25 or color_to_match[0] - 25 < \
                        br_color[0] < color_to_match[0] + 25:
                    i += 1
                else:
                    loc.pop(i)

        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)

        for pt in loc:

            tl = pt

            if 0 < title < 5:
                circles.append((tl[0], tl[1]))
            if 4 < title < 9:
                flowers.append((tl[0], tl[1]))
            if 42 <= title <= 43:
                gold.append((tl[0], tl[1]))

        shuffle(loc)

        press(flowers)
        press(circles)
        press(gold)

        k = 0
        if len(loc) % 2 == 0:
            for tile in loc:
                if title == 34:
                    mouse.move(tile[0] + 35, tile[1] + 35, True, 0.01)
                elif title == 12 or title == 14 or title == 15 or title == 17 or title == 18 or title == 44:
                    mouse.move(tile[0], tile[1], True, 0.01)
                else:
                    mouse.move(tile[0] + 25, tile[1] + 25, True, 0.01)

                mouse.click()

        elif len(loc) >= 3 and len(loc) % 2 == 1:
            while k != len(loc) - 1:
                pt = loc[k]
                if title == 34:
                    mouse.move(pt[0] + 30, pt[1] + 30, True, 0.01)
                if title == 12 or title == 14 or title == 15 or title == 17 or title == 18 or title == 44:
                    mouse.move(pt[0], pt[1], True, 0.01)
                else:
                    mouse.move(pt[0] + 25, pt[1] + 25, True, 0.01)
                mouse.click()
                k += 1

        if FM[i]:
            tile = cv2.imread(path)
            tile = cv2.cvtColor(tile, cv2.COLOR_BGR2RGB)

            sift = cv2.xfeatures2d.SIFT_create()
            kpsrc, dessrc = sift.detectAndCompute(tile, None)
            kpdest, desdest = sift.detectAndCompute(backg, None)

            bf = cv2.BFMatcher()
            matches = bf.knnMatch(dessrc, desdest, k=2)

            good = []
            for match1, match2 in matches:
                if match1.distance < 0.90 * match2.distance:
                    good.append([match1])

            tile_matches = cv2.drawMatchesKnn(tile, kpsrc, backg, kpdest, good, None, flags=2)

            goodpts = []
            g = 0
            while g != len(good):
                obj_unpack = good[g]
                obj = obj_unpack[0]
                tI = obj.trainIdx
                good_pt = kpdest[tI].pt
                goodpts.append(good_pt)
                g += 1
            goodpts.sort()

            i = 0
            while i != len(goodpts) - 1 and len(goodpts) != 0:
                cur_x, cur_y = goodpts[i]
                fut_x, fut_y = goodpts[i + 1]
                if (cur_x - 25 < fut_x < cur_x + 25) or (cur_y - 25 < fut_y < cur_y + 25):
                    goodpts.pop(i + 1)
                else:
                    i += 1

            badtiles = []
            for pt in goodpts:
                x, y = pt
                lpt = x - 30
                bpt = y - 30

                l_color = backg[int(y), int(lpt)]
                l_color = l_color[::-1]

                r_color = backg[int(bpt), int(x)]
                r_color = r_color[::-1]

                if not (20 <= pt[0] <= 1700 and 0 <= pt[1] <= 1000):
                    badtiles.append(pt)
                elif title != 17 and l_color[0] < 175 and r_color[0] < 175 and title != 42:
                    badtiles.append(pt)

            i = 0
            count = 0
            deleted = 0
            total = len(goodpts)

            while count != total:
                tile_x, tile_y = goodpts[i]
                popped = False

                for bad in badtiles:

                    bad_x = bad[0]
                    bad_y = bad[1]

                    if deleted != len(badtiles):
                        if tile_x == bad_x and tile_y == bad_y:
                            goodpts.pop(i)
                            popped = True
                            deleted += 1

                if not popped:
                    i += 1

                count += 1

            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)

            shuffle(goodpts)
            k = 0
            if len(goodpts) % 2 == 0:
                for tile in goodpts:
                    mouse.move(tile[0], tile[1], True, 0.01)
                    mouse.click()

            elif len(goodpts) >= 3 and len(goodpts) % 2 == 1:
                while k != len(goodpts) - 1:
                    pt = goodpts[k]
                    if title == 34:
                        mouse.move(pt[0] + 30, pt[1] + 30, True, 0.01)
                    if title == 12 or title == 14 or title == 15 or title == 18:
                        mouse.move(pt[0], pt[1], True, 0.01)
                    else:
                        mouse.move(pt[0] + 25, pt[1] + 25, True, 0.01)
                    mouse.click()
                    k += 1

    if cv2.waitKey(1) and 0xFF == 27:
        break

cv2.destroyAllWindows()
