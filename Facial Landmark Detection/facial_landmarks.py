import cv2
import dlib
import argparse
import numpy as np


def shape_to_np(shape):
    coords = np.zeros((68, 2), dtype="int")
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path of image")
ap.add_argument("-p", "--predictor", required=True, help="Path of landmark predictor")
ap.add_argument("-s", "--save", help="Path of the image that will be saved")
args = vars(ap.parse_args())

save = False
if args["save"] is not None and args["save"] == "True":
    save = True

image = cv2.imread(args["image"])
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["predictor"])

grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
face_coords = detector(grayscale, 1)

breaks = [16, 21, 26, 30, 35, 41, 47]

for face_coord in face_coords:
    shape = predictor(grayscale, face_coord)
    shape = shape_to_np(shape)
    prev_coord = tuple(shape[0])
    for i, (x, y) in enumerate(shape):
        cv2.line(image, prev_coord, (x, y), (255, 0, 0), 2)
        if i in breaks:
            prev_coord = tuple(shape[i + 1])
        else:
            prev_coord = (x, y)

        if i == 41:
            cv2.line(image, (x, y), tuple(shape[36]), (255, 0, 0), 2)
        elif i == 47:
            cv2.line(image, (x, y), tuple(shape[42]), (255, 0, 0), 2)

if save:
    cv2.imwrite(args["save"], image)
cv2.imshow("res", image)
cv2.waitKey(0)
