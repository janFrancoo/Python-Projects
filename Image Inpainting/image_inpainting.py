# esc - quit
# enter - accept the mask and inpaint
# r - clear the mask

import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path of the image")
ap.add_argument("-r", "--radius", required=True, help="Mask select radius")
ap.add_argument("-s", "--save", help="Path of the result")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = cv2.resize(image, (800, 600))
mask = np.zeros(image.shape[:2], dtype=np.uint8)
radius = int(args["radius"])


def draw_circle(event, x, y, _, __):
    global drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.circle(mask, (x, y), radius, 255, -1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False


drawing = False
window_name = "select mask"
cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name, draw_circle)

colored = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
colored[:, :, :] = 0
while True:
    zeroes = np.where(mask == 255)
    colored[zeroes[0], zeroes[1], 2] = 255
    combined = cv2.addWeighted(image, 1, colored, 0.5, 0)

    cv2.imshow(window_name, combined)
    cv2.imshow("blank", mask)
    if cv2.waitKey(20) & 0xFF == 27:
        break
    elif cv2.waitKey(20) & 0xFF == 13:
        inpainted = cv2.inpaint(image, mask, radius * 2, cv2.INPAINT_NS)
        cv2.imshow("res", inpainted)
        cv2.waitKey(0)

        if args["save"] is not None:
            cv2.imwrite(args["save"], inpainted)

        break
    elif cv2.waitKey(20) & 0xFF == 114:
        mask = np.zeros(image.shape[:2], dtype=np.uint8)

cv2.destroyAllWindows()
