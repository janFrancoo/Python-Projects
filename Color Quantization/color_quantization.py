import cv2
import argparse
import numpy as np
from sklearn.cluster import KMeans

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path of image")
ap.add_argument("-s", "--save", help="Path of image that will be saved")
ap.add_argument("-n", "--n_cluster", help="Number of clusters")
args = vars(ap.parse_args())

n_cluster = 3 if args["n_cluster"] is None else int(args["n_cluster"])
image = cv2.imread(args["image"])
k_means = KMeans(n_clusters=n_cluster)

reshaped = image.reshape((image.shape[0] * image.shape[1], 3))
labels = k_means.fit_predict(reshaped)
quant = k_means.cluster_centers_.astype("uint8")[labels]
quant = quant.reshape((image.shape[0], image.shape[1], 3))

cv2.imshow("n_cluster = " + str(n_cluster), np.hstack([image, quant]))
cv2.waitKey(0)

if args["save"] is not None:
    cv2.imwrite(args["save"], quant)
