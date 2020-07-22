import cv2
import argparse
import numpy as np
from skimage.util import img_as_float
from skimage.segmentation import slic


def get_coord(event, x, y, _, __):
    global coord_x, coord_y
    if event == cv2.EVENT_LBUTTONDOWN:
        coord_x = x
        coord_y = y


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path of the image")
ap.add_argument("-n", "--n_segments", help="Number of segments used in slic func")
args = vars(ap.parse_args())

image = img_as_float(cv2.imread(args["image"]))

num_segment = 50 if args["n_segments"] is None else int(args["n_segments"])
segments = slic(image, n_segments=num_segment, sigma=5)

window_name = "n_segments = " + str(num_segment)
cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name, get_coord)

coord_x = coord_y = 0
while True:
    selected_segment = segments[coord_y][coord_x]
    mask = np.zeros(image.shape[:2], dtype="uint8")
    mask[segments == selected_segment] = 255

    cv2.imshow(window_name, image)
    cv2.imshow("Selected segment", mask)
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
