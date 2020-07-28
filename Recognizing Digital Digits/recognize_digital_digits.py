import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path of the image")
args = vars(ap.parse_args())

DIGITS_LOOKUP = {
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
    (1, 0, 1, 1, 1, 1, 0): 2,
    (1, 0, 1, 1, 0, 1, 1): 3,
    (0, 1, 1, 1, 0, 1, 0): 4,
    (1, 1, 0, 1, 0, 1, 1): 5,
    (1, 1, 0, 1, 1, 1, 1): 6,
    (1, 0, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9
}


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def perspective_transform(img, points):
    width = height = 5
    bounds = order_points(points)
    top_left, top_right, bottom_right, bottom_left = bounds
    max_width = max(
        int(np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))),
        int(np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2))))
    max_height = max(
        int(np.sqrt(((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2))),
        int(np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))))
    width = max_width if max_width != 0 else width
    height = max_height if max_height != 0 else height
    dst = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(bounds, dst)
    transformed = cv2.warpPerspective(img, M, (width, height))
    return transformed


def recognize_digital_digit(cropped_digit):
    digit_w, digit_h = cropped_digit.shape
    if digit_w < 55:
        return 1

    dw, dh = (int(digit_w * 0.25), int(digit_h * 0.15))
    dhc = int(digit_h * 0.05)
    segments = [
        ((0, 0), (w, dh)),  # top
        ((0, 0), (dw, h // 2)),  # top-left
        ((w - dw, 0), (w, h // 2)),  # top-right
        ((0, (h // 2) - dhc), (w, (h // 2) + dhc)),  # center
        ((0, h // 2), (w, h)),  # bottom-left
        ((w - dh, h // 2), (w, h)),  # bottom-right
        ((0, h - dh), (w, h))  # bottom
    ]

    sections = [0] * len(segments)
    for i, ((a_x, a_y), (b_x, b_y)) in enumerate(segments):
        mask = cropped_digit[a_y:b_y, a_x:b_x]
        mask_area = (b_x - a_x) * (b_y - a_y)
        density = cv2.countNonZero(mask)

        if density / float(mask_area) > 0.5:
            sections[i] = 1

    return DIGITS_LOOKUP[tuple(sections)]


resized = cv2.imread(args["image"])

gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (7, 7), 0)
edged = cv2.Canny(blurred, 75, 150, 255)

contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

warped = None
for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    if len(approx) == 4:
        box = cv2.minAreaRect(c)
        corners = cv2.boxPoints(box)
        warped = perspective_transform(resized, corners)
        break

gray_warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
ths = cv2.threshold(gray_warped, 75, 255, cv2.THRESH_BINARY)[1]

cv2.imshow("ths", ths)
cv2.waitKey(0)

kernel = np.ones((3, 3))
erosion = cv2.erode(ths, kernel, iterations=2)

digits = []
contours_warped, _ = cv2.findContours(erosion, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
for c in contours_warped:
    x, y, w, h = cv2.boundingRect(c)
    if 20 <= w <= 55 and 50 <= h <= 60:
        digit = recognize_digital_digit(ths[y:y+h, x:x+w])
        digits.append(digit)

print(digits)
