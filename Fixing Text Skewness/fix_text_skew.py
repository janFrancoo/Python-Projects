import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path of image")
ap.add_argument("-s", "--show", help="If true result will be shown or false")
args = vars(ap.parse_args())

show = True if args["show"] == "true" else False
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

grad_x = cv2.Sobel(gray, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=-1)
gradient = cv2.convertScaleAbs(grad_x)

kernel = np.ones((5, 5))
dilation = cv2.dilate(gradient, kernel, iterations=5)

contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if len(contours) != 1:
    raise Exception("Bad process")

angle = cv2.minAreaRect(contours[0])[-1]
angle = 90 + angle if angle < -40 else angle

M = cv2.moments(contours[0])
center_x = int(M["m10"] / M["m00"])
center_y = int(M["m01"] / M["m00"])

h, w = image.shape[:2]
M = cv2.getRotationMatrix2D((center_x, center_y), angle, 1.0)
rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

if show:
    cv2.imshow("test", rotated)
    cv2.waitKey(0)

cv2.imwrite(args["image"].split(".")[0] + "_res.png", rotated)
