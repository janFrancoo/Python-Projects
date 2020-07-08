import pickle
import dataset
import argparse
from hog import HOG
from sklearn.svm import LinearSVC

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--train", required=True, help="train.csv path")
ap.add_argument("-m", "--model", required=True, help="path of where model will be saved")
args = vars(ap.parse_args())

digits, labels = dataset.load_digits(args["train"])
hog = HOG(orientations=18, pixels_per_cell=(6, 6), cells_per_block=(1, 1), transform=True)

data = []
for digit in digits:
    hist = hog.describe(digit)
    data.append(hist)

model = LinearSVC()
model.fit(data, labels)
pickle.dump(model, open(args["model"], 'wb'))
