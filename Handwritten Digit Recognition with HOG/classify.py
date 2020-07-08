import cv2
import pickle
import argparse
from hog import HOG

ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True, help="trained model path")
ap.add_argument("-i", "--image", required=True, help="image path")
args = vars(ap.parse_args())

model = pickle.load(open(args["model"], 'rb'))
hog = HOG(orientations=18, pixels_per_cell=(6, 6), cells_per_block=(1, 1), transform=True)

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 30, 150)

contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key=lambda x: x[1])

for (c, _) in contours:
    (x, y, w, h) = cv2.boundingRect(c)

    if w >= 4 and h >= 15:
        roi = gray[y:y + h, x:x + w]
        resized = cv2.resize(roi, (28, 28))
        hist = hog.describe(resized)
        digit = model.predict([hist])[0]

        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv2.putText(image, str(digit), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
        cv2.imshow("final", image)
        cv2.waitKey(0)

# with some image transformations on image during training and parameter tuning, result should be better
