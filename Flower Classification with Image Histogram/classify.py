import cv2
import pickle
import argparse
import numpy as np
from sklearn.preprocessing import LabelEncoder

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--saved", required=True, help="Path of saved model")
ap.add_argument("-f", "--flower", required=True, help="Path of image")
ap.add_argument("-m", "--mask", required=True, help="Path of mask")
args = vars(ap.parse_args())

model = pickle.load(open(args["saved"], 'rb'))
flower = cv2.imread(args["flower"])
mask = cv2.imread(args["mask"])
gray_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

label_encoder = LabelEncoder()
label_encoder.classes_ = np.load('classes.npy')
hist = cv2.calcHist([flower], [0, 1, 2], gray_mask, [8, 8, 8], [0, 256, 0, 256, 0, 256])
cv2.normalize(hist, hist)
flower_class = label_encoder.inverse_transform(model.predict([hist.flatten()]))[0]

print(flower_class)
cv2.imshow("flower", flower)
cv2.waitKey(0)
