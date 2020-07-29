import os
import cv2
import vptree
import pickle
import argparse
from image_hashing import get_hash, convert_hash, hamming

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--folder", required=True, help="Path of the folder")
ap.add_argument("-t", "--tree_out", required=True, help="Path for the output of vp-tree")
ap.add_argument("-d", "--dict_out", required=True, help="Path for the output of hash dict")
args = vars(ap.parse_args())

hashes = {}
for path, _, files in os.walk(args["folder"]):
    for file_name in files:
        image = cv2.imread(os.path.join(path, file_name))

        if image is None:
            continue

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_hash = convert_hash(get_hash(gray))

        # if hash is none, create list else update list
        hash_list = hashes.get(image_hash, [])
        hash_list.append(os.path.join(path, file_name))
        hashes[image_hash] = hash_list

points = list(hashes.keys())
vp_tree = vptree.VPTree(points, hamming)

f = open(args["tree_out"], 'wb')
f.write(pickle.dumps(vp_tree))
f.close()

f = open(args["dict_out"], 'wb')
f.write(pickle.dumps(hashes))
f.close()
