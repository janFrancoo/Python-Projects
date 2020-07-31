import cv2
import argparse
from pyzbar import pyzbar

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path of the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

barcodes = pyzbar.decode(image)

for barcode in barcodes:
    x, y, w, h = barcode.rect
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    data = barcode.data.decode("utf-8")
    barcode_type = barcode.type

    cv2.putText(image, str(data), (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    print(barcode_type, data)

cv2.imshow("res", image)
cv2.waitKey(0)
