import os
import cv2
import dlib
import argparse
import numpy as np
from random import shuffle

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", required=True, help="Directory of faces")
ap.add_argument("-s", "--shape_predictor", required=True, help="Path of shape predictor")
ap.add_argument("-c", "--haar_cascade", required=True, help="Path of Haar Cascade classifier")
ap.add_argument("-m", "--mask", required=True, help="Path of mask png image")
args = vars(ap.parse_args())


def get_dlib_rect(coords):
    left = coords[0]
    top = coords[1]
    right = coords[0] + coords[2]
    bottom = coords[1] + coords[3]
    dlib_rect = dlib.rectangle(left, top, right, bottom)
    return dlib_rect


def shape_to_np(shape):
    coords = np.zeros((68, 2), dtype="int")
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords


images = [[cv2.imread(os.path.join(args["face"], file_name)), file_name] for file_name in os.listdir(args["face"])]
face_cascade = cv2.CascadeClassifier(args["haar_cascade"])
predictor = dlib.shape_predictor(args["shape_predictor"])
mask = cv2.imread(args["mask"], -1)

masked = 0
limit = int(len(images) / 2)
shuffle(images)
for image, file_name in images:
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_rects = face_cascade.detectMultiScale(grayscale, scaleFactor=1.3, minNeighbors=5)

    if len(face_rects) != 1:
        continue
    x, y, w, h = face_rects[0][0], face_rects[0][1], face_rects[0][2], face_rects[0][3]

    shape = predictor(grayscale, get_dlib_rect([x, y, w, h]))
    shape = shape_to_np(shape)

    chin_width = shape[16][0] - shape[0][0]
    chin_height = shape[8][1] - shape[29][1]
    resized_mask = cv2.resize(mask, (chin_width, chin_height))
    # calculate rotation and rotate resized_mask

    alpha_s = resized_mask[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    masked_face = image[y:y+h, x:x+w]
    off_y = shape[0][1] - y
    off_y_h = off_y + resized_mask.shape[0]
    off_x = shape[0][0] - x
    off_x_w = off_x + resized_mask.shape[1]

    try:
        for c in range(0, 3):
            masked_face[off_y:off_y_h, off_x:off_x_w, c] = (alpha_s * resized_mask[:, :, c] +
                                                            alpha_l * masked_face[off_y:off_y_h, off_x:off_x_w, c])
        cv2.imwrite(os.path.join(args["face"], ("masked_" + str(masked) + ".jpg")), masked_face)
        os.remove(os.path.join(args["face"], file_name))
        masked += 1
    except:
        pass

    if masked == limit:
        break
