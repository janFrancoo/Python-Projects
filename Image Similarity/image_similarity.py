import cv2
import argparse
import numpy as np
from skimage.measure import compare_ssim


def mean_squared_error(image_a, image_b):
    if image_a.shape[0] != image_b.shape[0] or image_a.shape[1] != image_b.shape[1]:
        raise Exception("Image dimensions are not same")
    return np.sum((image_a.astype("float32") - image_b.astype("float32")) ** 2) / float(image_a.shape[0] *
                                                                                        image_b.shape[1])


def show_result(image_a, image_b, title):
    cv2.imshow(title, np.hstack([image_a, image_b]))
    cv2.waitKey(0)
    cv2.imwrite("data/mse_12580_ssim_0_115.jpg", np.hstack([image_a, image_b]))


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image_original", required=True, help="Path of the image one")
ap.add_argument("-t", "--image_target", required=True, help="Path of the image two")
ap.add_argument("-s", "--show", help="A boolean value that allows image to show")
ap.add_argument("-m", "--method", help="structural_similarity or mean_squared_error")
args = vars(ap.parse_args())

show = True if args["show"] is not None and args["show"] == "True" else False
image_original = cv2.imread(args["image_original"], 0)
image_target = cv2.imread(args["image_target"], 0)

if args["method"] is None:
    mse = mean_squared_error(image_original, image_target)
    ssim = compare_ssim(image_original, image_target)
    print("MSE:", mse, "SSIM:", ssim)
    if show:
        show_result(image_original, image_target, "MSE: " + str(mse) + " SSIM: " + str(ssim))
elif args["method"] == "mean_squared_error":
    mse = mean_squared_error(image_original, image_target)
    print("MSE:", mse)
    if show:
        show_result(image_original, image_target, "MSE: " + str(mse))
elif args["method"] == "structural_similarity":
    ssim = compare_ssim(image_original, image_target)
    print("SSIM:", ssim)
    if show:
        show_result(image_original, image_target, "SSIM: " + str(ssim))
else:
    raise Exception("Unknown method")
