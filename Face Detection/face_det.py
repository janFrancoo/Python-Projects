import cv2
import argparse
from face_detector import FaceDetector

ap = argparse.ArgumentParser()
ap.add_argument("-c ", "--cascade", required=True, help="cascade path")
ap.add_argument("-i", "--image", required=True, help="image path")
ap.add_argument("-s", "--show", help="show result")
args = vars(ap.parse_args())

show = False

img = cv2.imread(args["image"])
face_cascade = cv2.CascadeClassifier(args["cascade"])

if args["show"] is not None:
    if args["show"].lower() in ('yes', 'true', 't', 'y', '1'):
        show = True
    elif args["show"].lower() in ('no', 'false', 'f', 'n', '0'):
        show = False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

face_detector = FaceDetector(face_cascade)
rects = face_detector.detect_faces(img, 1.1, 5)
print(rects)

if show:
    for (x, y, w, h) in rects:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)

    cv2.imshow('img', img)
    cv2.waitKey(0)
