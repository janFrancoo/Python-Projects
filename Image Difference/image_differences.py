import cv2
import argparse
import numpy as np
from skimage.measure import compare_ssim

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--image_first", required=True, help="Path of the first image")
ap.add_argument("-s", "--image_second", required=True, help="Path of the second image")
ap.add_argument("-l", "--show", help="true if the result will be shown")
ap.add_argument("-w", "--save", help="Path of the result image that will be saved")
args = vars(ap.parse_args())

show = True if args["show"] is not None and args["show"] == "true" else False
image_first = cv2.imread(args["image_first"])
image_second = cv2.imread(args["image_second"])

gray_first = cv2.cvtColor(image_first, cv2.COLOR_BGR2GRAY)
gray_second = cv2.cvtColor(image_second, cv2.COLOR_BGR2GRAY)

score, diff = compare_ssim(gray_first, gray_second, full=True)
diff = (diff * 255).astype("uint8")
print("SSIM:", score)

ths = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
contours, _ = cv2.findContours(ths, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(image_first, (x, y), (x + w, y + h), (0, 255, 0), 1)
    cv2.rectangle(image_second, (x, y), (x + w, y + h), (0, 255, 0), 1)

res = np.hstack([image_first, image_second])

if show:
    cv2.imshow("res", res)
    cv2.waitKey(0)

if args["save"] is not None:
    cv2.imwrite(args["save"], res)
