import cv2
import numpy as np

image = cv2.imread("data/pisa.jpg", 0)

noised = image.copy()
mask = np.random.randint(0, 2, (image.shape[0], image.shape[1]))
noised[mask == 1] = 0
cv2.imwrite("data/pisa_noise.jpg", noised)

contrast = image.copy()
for y in range(image.shape[0]):
    for x in range(image.shape[1]):
        contrast[y, x] = np.clip(1.5 * image[y, x] + 30, 0, 255)
cv2.imwrite("data/pisa_contrast.jpg", contrast)
