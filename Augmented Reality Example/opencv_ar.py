import sys
import cv2
import imutils
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True)
ap.add_argument("-s", "--source", required=True)
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = imutils.resize(image, width=600)
source = cv2.imread(args["source"])
img_h, img_w = image.shape[:2]
src_h, src_w = source.shape[:2]

aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
aruco_params = cv2.aruco.DetectorParameters_create()
corners, ids, _ = cv2.aruco.detectMarkers(image, aruco_dict, parameters=aruco_params)

if len(corners) != 4:
    sys.exit(0)

ids = ids.flatten()
ref_pts = []

for i in (923, 1001, 241, 1007):
    j = np.squeeze(np.where(ids == i))
    corner = np.squeeze(corners[j])
    ref_pts.append(corner)

ref_pt_tl, ref_pt_tr, ref_pt_br, ref_pt_bl = ref_pts
dst_mat = [ref_pt_tl[0], ref_pt_tr[1], ref_pt_br[2], ref_pt_bl[3]]
dst_mat = np.array(dst_mat)
src_mat = np.array([[0, 0], [src_w, 0], [src_w, src_h], [0, src_h]])

h, _ = cv2.findHomography(src_mat, dst_mat)
warped = cv2.warpPerspective(source, h, (img_w, img_h))

mask = np.zeros((img_h, img_w), dtype="uint8")
cv2.fillConvexPoly(mask, dst_mat.astype("int32"), (255, 255, 255), cv2.LINE_AA)

mask_scaled = mask.copy() / 255.0
mask_scaled = np.dstack([mask_scaled] * 3)

warped_multiplied = cv2.multiply(warped.astype("float"), mask_scaled)
image_multiplied = cv2.multiply(image.astype(float), 1.0 - mask_scaled)
output = cv2.add(warped_multiplied, image_multiplied)
output = output.astype("uint8")

cv2.imshow("RESULT", output)
cv2.waitKey(0)

cv2.imwrite("result.jpg", output)
