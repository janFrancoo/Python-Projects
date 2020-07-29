import os
import cv2
import argparse
from image_hashing import get_hash

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path of the image")
ap.add_argument("-f", "--folder", required=True, help="Path of the folder")
ap.add_argument("-t", "--thresh", help="Thresh value for hash similarity")
args = vars(ap.parse_args())

ths = 30 if args["thresh"] is None else int(args["thresh"])
image = cv2.imread(args["image"])

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image_hash = get_hash(gray)

match = []
for file_name in os.listdir(args["folder"]):
    image = cv2.imread(os.path.join(args["folder"], file_name))

    if image is None:
        continue

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    im_hash = get_hash(gray)

    if im_hash == image_hash:
        match.append(file_name)

print(match)
