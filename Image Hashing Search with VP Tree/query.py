import cv2
import pickle
import argparse
import numpy as np
from image_hashing import get_hash, convert_hash

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path of the image")
ap.add_argument("-t", "--tree", required=True, help="Path of the vp tree")
ap.add_argument("-d", "--dict", required=True, help="Path of the hash dict")
ap.add_argument("-l", "--limit", default=10, help="Threshold value for hamming distance")
ap.add_argument("-s", "--show", default=False, help="Threshold value for hamming distance")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
vp_tree = pickle.loads(open(args["tree"], "rb").read())
hashes = pickle.loads(open(args["dict"], "rb").read())

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image_hash = convert_hash(get_hash(gray))

result = vp_tree.get_all_in_range(image_hash, int(args["limit"]))
sorted_result = sorted(result)

for d, h in sorted_result:
    similar_images = hashes.get(h, [])
    for similar_image_path in similar_images:
        print(similar_image_path)

        if args["show"] is not None and args["show"] == "true":
            similar_image = cv2.imread(similar_image_path)

            if image.shape[0] == similar_image.shape[0]:
                cv2.imshow(str(d), np.hstack([image, similar_image]))
                cv2.waitKey(0)
            elif image.shape[0] > similar_image.shape[0]:
                blank_image = np.zeros((image.shape[0], similar_image.shape[1], 3), np.uint8)
                blank_image[0:similar_image.shape[0], :] = similar_image
                cv2.imshow(str(d), np.hstack([image, blank_image]))
                cv2.waitKey(0)
            else:
                blank_image = np.zeros((similar_image.shape[0], image.shape[1], 3), np.uint8)
                blank_image[0:image.shape[0], :] = image
                cv2.imshow(str(d), np.hstack([blank_image, similar_image]))
                cv2.waitKey(0)
