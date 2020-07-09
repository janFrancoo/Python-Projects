import cv2
import pickle
import dataset
import argparse
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--flower", required=True, help="Path of images")
ap.add_argument("-m", "--mask", required=True, help="Path of masks")
ap.add_argument("-s", "--save", required=True, help="Path of model that will be saved")
args = vars(ap.parse_args())

flowers, masks, classes = dataset.get_flowers(args["flower"], args["mask"])

data = []
for flower, mask in zip(flowers, masks):
    hist = cv2.calcHist([flower], [0, 1, 2], mask, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    data.append(hist.flatten())

label_encoder = LabelEncoder()
label_encoder.fit(classes)
np.save('classes.npy', label_encoder.classes_)
target = label_encoder.transform(classes)

x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.3)

forest = RandomForestClassifier(n_estimators=25)
forest.fit(x_train, y_train)
pickle.dump(forest, open(args["save"], 'wb'))
