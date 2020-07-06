import cv2
import argparse
from face_detector import FaceDetector

ap = argparse.ArgumentParser()
ap.add_argument("-c ", "--cascade", required=True, help="cascade path")
ap.add_argument("-s", "--scale", help="scale percent for frames")
args = vars(ap.parse_args())

scale_percent = 100
if args["scale"] is not None:
    scale_percent = int(args["scale"])

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(args["cascade"])
face_detector = FaceDetector(face_cascade)

ret, frame = cap.read()
width = int(frame.shape[1] * scale_percent / 100)
height = int(frame.shape[0] * scale_percent / 100)

while True:
    ret, frame = cap.read()
    if ret is None:
        break

    resized = cv2.resize(frame, (width, height))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = face_detector.detect_faces(gray, 1.1, 5)

    for (x, y, w, h) in rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 4)

    cv2.imshow('img', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
