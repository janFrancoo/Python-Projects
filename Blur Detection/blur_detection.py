import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path of the image")
ap.add_argument("-t", "--threshold", help="Threshold value")
args = vars(ap.parse_args())

threshold = 25 if args["threshold"] is None else args["threshold"]
image = cv2.imread(args["image"])

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
val = cv2.Laplacian(gray, cv2.CV_8U).var()

if val < threshold:
    print("Blurry", val)
else:
    print("Not blurry", val)
