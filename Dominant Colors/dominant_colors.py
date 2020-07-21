import cv2
import argparse
import numpy as np
from sklearn.cluster import KMeans

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Image path")
ap.add_argument("-n", "--n_cluster", required=True, help="Image path")
args = vars(ap.parse_args())

n_cluster = int(args["n_cluster"])
image = cv2.imread(args["image"])
image_name = args["image"].split("/")[::-1]

reshaped_image = image.reshape((image.shape[0] * image.shape[1], 3))

k_means = KMeans(n_clusters=n_cluster)
k_means.fit(reshaped_image)

num_labels = np.arange(0, len(np.unique(k_means.labels_)) + 1)
hist, _ = np.histogram(k_means.labels_, bins=num_labels)

hist = hist.astype("float")
hist /= hist.sum()
hist[::-1].sort()

last_width = 0
dom_color_shape = (100, 600)
dom_colors = np.zeros([dom_color_shape[0], dom_color_shape[1], 3])
for i, color in enumerate(k_means.cluster_centers_):
    width = int(hist[i] * dom_color_shape[1])
    dom_colors[:, last_width:last_width+width, 0] = np.ones([dom_color_shape[0], width]) * color[0] / 255.0
    dom_colors[:, last_width:last_width+width, 1] = np.ones([dom_color_shape[0], width]) * color[1] / 255.0
    dom_colors[:, last_width:last_width+width, 2] = np.ones([dom_color_shape[0], width]) * color[2] / 255.0
    last_width += width

cv2.imshow("image", image)
cv2.imshow("dom_colors", dom_colors)
cv2.waitKey()

cv2.imwrite("data/dom_colors_" + image_name[0] + ".jpg", dom_colors)
