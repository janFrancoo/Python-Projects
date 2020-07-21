import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True, help="Source image path")
ap.add_argument("-t", "--target", required=True, help="Target image path")
args = vars(ap.parse_args())

source = cv2.imread(args["source"])
target = cv2.imread(args["target"])
target_name = args["target"].split("/")[::-1][0]

source_lab = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
target_lab = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")

source_lab_channels = []
target_lab_channels = []
for i in range(3):
    source_lab_channels.append(source_lab[:, :, i])
    target_lab_channels.append(target_lab[:, :, i])

source_lab_std = np.std(source_lab_channels)
source_lab_mean = np.mean(source_lab_channels)
target_lab_std = np.std(target_lab_channels)
target_lab_mean = np.mean(target_lab_channels)

target_lab_channels_transfer = []
for i, c in enumerate(target_lab_channels):
    diff_mean = c - target_lab_mean
    scaled = diff_mean * (target_lab_std / source_lab_std)
    mean_added = scaled + source_lab_mean
    clipped = np.clip(mean_added, 0, 255)
    target_lab_channels_transfer.append(clipped)

merged = cv2.merge(target_lab_channels_transfer)
to_rgb = cv2.cvtColor(merged.astype("uint8"), cv2.COLOR_LAB2BGR)

cv2.imshow("source", source)
cv2.imshow("target", target)
cv2.imshow("final", to_rgb)
cv2.imwrite("data/transferred_" + target_name, to_rgb)
cv2.waitKey(0)
