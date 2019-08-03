import cv2
import matplotlib.pyplot as plt

img = cv2.imread('spongebob.png')
img2show = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
plt.imshow(img2show)
plt.show()

blurredImg = cv2.GaussianBlur(img, (11, 11), 15)
img2how = cv2.cvtColor(blurredImg, cv2.COLOR_RGB2BGR)
plt.imshow(img2how)
plt.show()

grayImg = cv2.cvtColor(blurredImg, cv2.COLOR_RGB2GRAY)
plt.imshow(grayImg, cmap='gray')
plt.show()

_, threshold = cv2.threshold(grayImg, 130, 255, cv2.THRESH_BINARY)
plt.imshow(threshold, cmap='gray')
plt.show()

laplace = cv2.Laplacian(threshold, -1, ksize=7)
plt.imshow(laplace, cmap='gray')
plt.show()

_, contours, hierarchy = cv2.findContours(laplace, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
sortedContours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
x, y, w, h = cv2.boundingRect(sortedContours[1])
cv2.rectangle(img2show, (x, y), (x + w, y + h), (0, 255, 0), 8)
x, y, w, h = cv2.boundingRect(sortedContours[2])
cv2.rectangle(img2show, (x, y), (x + w, y + h), (255, 0, 0), 8)
plt.imshow(img2show)
plt.show()
