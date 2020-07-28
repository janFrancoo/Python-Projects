import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path of the image")
ap.add_argument("-s", "--show", help="Show image if true else false")
args = vars(ap.parse_args())

show = True if args["show"] is not None and args["show"] == "true" else False
image = cv2.imread(args["image"])
B, G, R = cv2.split(image.astype("float"))

rg = np.absolute(R - G)
yb = np.absolute((R + G) / 2 - B)
std_rgyb = (np.std(rg) ** 2 + np.std(yb) ** 2) ** (1/2)
mean_rgyb = (np.mean(rg) ** 2 + np.mean(yb) ** 2) ** (1/2)
colorfulness = std_rgyb + 0.3 * mean_rgyb

if show:
    cv2.putText(image, "Colorfulness: " + str(colorfulness), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
    cv2.imshow("res", image)
    cv2.imwrite("data/strawberry_res.jpg", image)
    cv2.waitKey(0)

print(colorfulness)
