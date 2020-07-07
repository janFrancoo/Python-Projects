import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="optional video path")
args = vars(ap.parse_args())

if args["video"] is None:
    cam = cv2.VideoCapture(0)
else:
    cam = cv2.VideoCapture(["video"])


def draw_rect(event, x, y, _, __):
    global point_1, point_2, click_counter, extract
    if event == cv2.EVENT_LBUTTONDOWN:
        extract = False
        click_counter = (click_counter + 1) % 3
        if click_counter == 1:
            point_1 = (x, y)
            point_2 = (x, y)
        elif click_counter == 2:
            extract = True
    elif event == cv2.EVENT_MOUSEMOVE and click_counter == 1:
        point_2 = (x, y)


def extract_lower_higher(image):
    avg_color_per_row = np.average(image, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    lower_c = avg_color / 1.3
    higher_c = avg_color * 1.3
    return lower_c, higher_c


target = False
extract = False
point_1 = (0, 0)
point_2 = (0, 0)
click_counter = 0
lower = higher = []
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", draw_rect)

while True:
    ret, frame = cam.read()

    if ret is None:
        break

    cv2.rectangle(frame, point_1, point_2, (0, 0, 255), 3)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    if extract:
        cropped = frame[point_1[1]:point_2[1], point_1[0]:point_2[0]]
        lower, higher = extract_lower_higher(cropped)
        point_1 = (0, 0)
        point_2 = (0, 0)
        click_counter += 1
        extract = False
        target = True

    if not target:
        continue

    color = cv2.inRange(frame, lower, higher)
    filtered_color = cv2.GaussianBlur(color, (5, 5), 3)

    contours, _ = cv2.findContours(filtered_color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        cnt = sorted(contours, key=cv2.contourArea, reverse=True)[0]
        rect = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt)))
        cv2.polylines(frame, [rect], False, (0, 255, 0), 2)

    cv2.imshow("Frame", frame)
    cv2.imshow("Binary", filtered_color)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cam.release()
cv2.destroyAllWindows()
