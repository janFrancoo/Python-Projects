import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path of image")
args = vars(ap.parse_args())

colors = {
    "blue": (255, 0, 0),
    "green": (0, 255, 0),
    "red": (51, 51, 255),
    "yellow": (0, 255, 255),
    "orange": (0, 128, 255),
}
shapes = ["tri", "rect", "pentagon"]


def evaluate_contour(cont):
    peri = cv2.arcLength(cont, True)
    approx = cv2.approxPolyDP(cont, 0.04 * peri, True)
    if 3 <= len(approx) <= 5:
        return shapes[len(approx) - 3]
    return "circle"


def distance(col_a, col_b):
    return ((col_a[0] - col_b[0]) ** 2 + (col_a[1] - col_b[1]) ** 2 + (col_a[2] - col_b[2]) ** 2) ** 1/3


def get_color(img, m):
    b, g, r, _ = cv2.mean(img, m)
    col = [b, g, r]
    min_col = ""
    min_val = 999999
    for i, color in enumerate(colors):
        dist = distance(colors[color], col)
        if dist < min_val:
            min_col = color
            min_val = dist
    return min_col


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
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
_, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    if cv2.contourArea(c) > 10:
        mask = np.zeros(gray.shape, np.uint8)
        cv2.drawContours(mask, [c], -1, 255, -1)
        s_color = get_color(image, mask)
        shape = evaluate_contour(c)

        M = cv2.moments(c)
        center_x = int(M["m10"] / M["m00"])
        center_y = int(M["m01"] / M["m00"])

        box = cv2.minAreaRect(c)
        corners = cv2.boxPoints(box)
        tl, _, __, ___ = order_points(corners)
        cv2.putText(image, s_color + " " + shape, (int(tl[0]) - 25, int(tl[1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.circle(image, (center_x, center_y), 5, (255, 255, 255), -1)

cv2.imshow("res", image)
cv2.waitKey(0)
cv2.imwrite(args["image"].split(".")[0] + "_res.jpg", image)
