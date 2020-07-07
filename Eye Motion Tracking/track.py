import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-e", "--eye", required=True, help="eye cascade path")
ap.add_argument("-f", "--face", required=True, help="frontal face cascade path")
ap.add_argument("-v", "--video", help="optional video path")
args = vars(ap.parse_args())

if args["video"] is not None:
    cam = cv2.VideoCapture(args["video"])
else:
    cam = cv2.VideoCapture(0)

eye_cascade = cv2.CascadeClassifier(args["eye"])
face_cascade = cv2.CascadeClassifier(args["face"])

while True:
    ret, frame = cam.read()

    if ret is None:
        break

    face_rects = face_cascade.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=5)
    roi = np.zeros((300, 300, 3), np.uint8)

    # for (x, y, w, h) in face_rects:
    #    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    if len(face_rects) == 1:
        face = face_rects[0]
        cropped = frame[face[1]:face[1]+face[3], face[0]:face[0]+face[2]]
        eye_rects = eye_cascade.detectMultiScale(cropped, scaleFactor=3, minNeighbors=7)

        # for (x, y, w, h) in eye_rects:
        #     cv2.rectangle(frame, (face[0] + x, face[1] + y),
        #                   (face[0] + x + w, face[1] + y + h), (0, 255, 0), 3)

        if len(eye_rects) > 0:
            (x, y, w, h) = eye_rects[0]
            one_eye = frame[face[1] + y:face[1] + y + h, face[0] + x:face[0] + x + w]

            factor = 7
            width = int(one_eye.shape[1] * factor)
            height = int(one_eye.shape[0] * factor)

            roi_large = cv2.resize(one_eye, (width, height))
            quart_h = int(height/2.7)
            quart_w = int(width/3.5)
            half_h = int(height/3)
            half_w = int(width/2)
            roi = roi_large[quart_h:quart_h + half_h, quart_w:quart_w + half_w]
            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            filtered_gray_roi = cv2.GaussianBlur(gray_roi, (7, 7), 0)
            _, thresh = cv2.threshold(filtered_gray_roi, 25, 255, type=cv2.THRESH_BINARY_INV)
            rows, cols = thresh.shape

            cv2.imshow("gray", filtered_gray_roi)
            cv2.imshow("thresh", thresh)

            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            if len(contours) > 0:
                (x, y, w, h) = cv2.boundingRect(contours[0])
                cv2.line(roi, (x + int(w / 2), 0), (x + int(w / 2), rows), (0, 255, 0), 2)
                cv2.line(roi, (0, y + int(h / 2)), (cols, y + int(h / 2)), (0, 255, 0), 2)

    cv2.imshow("One Eye", roi)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
