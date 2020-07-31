import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path of the image")
ap.add_argument("-c", "--cascade", required=True, help="Path of frontal face Haar Cascade")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = cv2.resize(image, (600, 600))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

"""
haar_cascade = cv2.CascadeClassifier(args["cascade"])

faces = haar_cascade.detectMultiScale(gray)

for x, y, w, h in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imshow("face detect", image)
cv2.waitKey(0)
"""

mask = np.zeros(image.shape[:2], dtype="uint8")
foreground = np.zeros((1, 65), dtype="float")
background = np.zeros((1, 65), dtype="float")

"""
for rect in faces:
    mask, background_model, foreground_model = cv2.grabCut(image, mask, rect, background, foreground, iterCount=10,
                                                           mode=cv2.GC_INIT_WITH_RECT)
    value_mask = (mask == cv2.GC_PR_FGD).astype("uint8") * 255
    cv2.imshow("Probable background", value_mask)
    cv2.waitKey(0)

"""

rect = (129, 73, 364, 339)  # Haar Cascade returns a much more smaller rectangle
mask, background_model, foreground_model = cv2.grabCut(image, mask, rect, background, foreground, iterCount=10, 
                                                       mode=cv2.GC_INIT_WITH_RECT)
value_mask = (mask == cv2.GC_PR_FGD).astype("uint8") * 255
cv2.imwrite("data/res_mask.jpg", value_mask)
cv2.imshow("Probable background", value_mask)

output_mask = (np.where((mask == cv2.GC_BGD) | (mask == cv2.GC_PR_BGD), 0, 1) * 255).astype("uint8")
output = cv2.bitwise_and(image, image, mask=output_mask)

cv2.imwrite("data/res.jpg", output)
cv2.imshow("res", output)
cv2.waitKey(0)

cv2.destroyAllWindows()
