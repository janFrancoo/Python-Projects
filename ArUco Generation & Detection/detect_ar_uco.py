import sys
import cv2
import argparse
from util import ARUCO_DICT
from util import line_color, line_width, circle_radius, circle_color, circle_width

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True)
ap.add_argument("-t", "--type", default="DICT_ARUCO_ORIGINAL")
args = vars(ap.parse_args())

if ARUCO_DICT.get(args["type"], None) is None:
    print(args["type"], "not supported")
    sys.exit(0)

image = cv2.imread(args["input"])
aruco_dict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
aruco_params = cv2.aruco.DetectorParameters_create()
corners, ids, _ = cv2.aruco.detectMarkers(image, aruco_dict, parameters=aruco_params)

if len(corners) > 0:
    ids = ids.flatten()
    for marker_corner, marker_id in zip(corners, ids):
        corners = marker_corner.reshape((4, 2))
        tl, tr, br, bl = corners
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))
        tl = (int(tl[0]), int(tl[1]))

        cv2.line(image, tl, tr, line_color, line_width)
        cv2.line(image, tl, bl, line_color, line_width)
        cv2.line(image, bl, br, line_color, line_width)
        cv2.line(image, br, tr, line_color, line_width)

        cx = int((tl[0] + br[0]) / 2.0)
        cy = int((tl[1] + br[1]) / 2.0)
        cv2.circle(image, (cx, cy), circle_radius, circle_color, circle_width)

        cv2.imshow("OUTPUT", image)
        cv2.waitKey(0)
