import cv2
import json
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path of the image")
ap.add_argument("-a", "--answers", required=True, help="Path of the answers json file")
ap.add_argument("-s", "--show", help="Show result if true else false")
ap.add_argument("-w", "--save", help="Save path for result")
args = vars(ap.parse_args())

show = True if args["show"] is not None and args["show"] == "true" else False
file = open(args["answers"], 'r')
answers = json.loads(file.read())
n_question = len(answers)
choices = ['A', 'B', 'C', 'D', 'E']


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
edged = cv2.Canny(blurred, 50, 200)

contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)
box = cv2.minAreaRect(contours[0])
corners = cv2.boxPoints(box)

width = height = 5
bounds = order_points(corners)
top_left, top_right, bottom_right, bottom_left = bounds
max_width = max(int(np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))),
                int(np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2))))
max_height = max(int(np.sqrt(((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2))),
                 int(np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))))
width = max_width if max_width != 0 else width
height = max_height if max_height != 0 else height
dst = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype="float32")
M = cv2.getPerspectiveTransform(bounds, dst)
warped = cv2.warpPerspective(image, M, (width, height))

gray_warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
ths = cv2.threshold(gray_warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

contours, _ = cv2.findContours(ths, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
circles = []
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    ar = w / float(h)
    if w >= 20 and h >= 20 and 0.9 <= ar <= 1.1:
        circles.append(c)

questions = []
circles_top_to_bottom = sorted(circles, key=lambda cntr: cv2.boundingRect(cntr)[1])
for i in np.arange(0, len(circles), 5):
    questions.append(circles_top_to_bottom[i:i+5])

correct = 0
for i, question in enumerate(questions, start=1):
    right_answer = answers[str(i)]
    circles_left_to_right = sorted(question, key=lambda cntr: cv2.boundingRect(cntr)[0])
    for j, circle in enumerate(circles_left_to_right):
        mask = np.zeros(ths.shape, dtype="uint8")
        cv2.drawContours(mask, [circle], -1, 255, -1)
        mask = cv2.bitwise_and(ths, ths, mask=mask)
        total = cv2.countNonZero(mask)

        if total > 500:
            cv2.drawContours(warped, [circle], -1, (0, 0, 255), 2)
            if choices.index(right_answer) == j:
                correct += 1

        if choices.index(right_answer) == j:
            cv2.drawContours(warped, [circle], -1, (0, 255, 0), 2)


total = 100 * correct / n_question
cv2.putText(warped, str(total), (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2)
print(total)

if show:
    cv2.imshow("res", warped)
    cv2.waitKey(0)

if args["save"] is not None:
    cv2.imwrite(args["save"], warped)
