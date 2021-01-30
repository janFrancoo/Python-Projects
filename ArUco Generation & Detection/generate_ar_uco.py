import sys
import cv2
import argparse
import numpy as np
from util import ARUCO_DICT

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output")
ap.add_argument("-i", "--id", type=int, required=True)
ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL")
ap.add_argument("-s", "--size", type=int, default=300)
args = vars(ap.parse_args())

if ARUCO_DICT.get(args["type"], None) is None:
    print(args["type"], "not supported")
    sys.exit(0)

aruco_dict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
tag = np.zeros((args["size"], args["size"], 1), dtype="uint8")
cv2.aruco.drawMarker(aruco_dict, args["id"], args["size"], tag, 1)

if args["output"] is None:
    cv2.imshow("GENERATED ARUCO", tag)
    cv2.waitKey(0)
else:
    cv2.imwrite(args["output"], tag)
