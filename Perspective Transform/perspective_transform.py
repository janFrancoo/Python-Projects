import cv2
import argparse
import numpy as np


def get_corners(event, x, y, _, __):
    global idx, resized, coord_x, coord_y
    if event == cv2.EVENT_LBUTTONDOWN:
        coord_x = x
        coord_y = y
        cv2.circle(resized, (x, y), 3, (0, 255, 0), -1)
        idx = (idx + 1) % 4


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path of the image")
ap.add_argument("-s", "--save", help="Path of the warped image that will be saved")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
resized = cv2.resize(image, (500, 500))

idx = 0
width = height = 5
coord_x = coord_y = 0
points = np.zeros((4, 2))
window_name = "Select borders"
cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name, get_corners)
while True:
    points[idx] = (coord_x, coord_y)
    bounds = order_points(points)
    top_left, top_right, bottom_right, bottom_left = bounds
    max_width = max(int(np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))),
                    int(np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2))))
    max_height = max(int(np.sqrt(((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2))),
                     int(np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))))
    width = max_width if max_width != 0 else width
    height = max_height if max_height != 0 else height
    dst = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(bounds, dst)
    warped = cv2.warpPerspective(resized, M, (width, height))

    cv2.imshow("res", warped)
    cv2.imshow(window_name, resized)
    if cv2.waitKey(20) & 0xFF == 27:
        if args["save"] is not None:
            cv2.imwrite(args["save"], warped)
        break

cv2.destroyAllWindows()
