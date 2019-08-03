import cv2
import numpy as np


def change_pixels(_):
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            for c in range(img.shape[2]):
                new_image[y, x, c] = np.clip(alpha * img[y, x, c] + beta, 0, 255)


img = cv2.imread('rabbit.jpg')
img = cv2.resize(img, (450, 500))
new_image = np.zeros(img.shape, img.dtype)
cv2.namedWindow("Trackbar")
cv2.createTrackbar("Alpha", "Trackbar", 1, 3, change_pixels)
cv2.createTrackbar("Beta", "Trackbar", 0, 100, change_pixels)

while True:
    cv2.imshow("Trackbar", new_image)

    if cv2.waitKey(1) & 0xFF == 27:
        break

    alpha = cv2.getTrackbarPos("Alpha", "Trackbar")
    beta = cv2.getTrackbarPos("Beta", "Trackbar")

cv2.destroyAllWindows()
