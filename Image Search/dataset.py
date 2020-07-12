import os
import cv2
from feature_extract import FeatureExtract


def get_images(path):
    images = []
    for file_name in os.listdir(path):
        images.append({
            "image": cv2.imread(os.path.join(path, file_name)),
            "file_name": file_name
        })
    return images


def get_data(path):
    data = []
    images = get_images(path)
    for obj in images:
        feat_extract = FeatureExtract(obj["image"])
        kp, des = feat_extract.extract_features()
        data_obj = {"des": des}
        data_obj.update(obj)
        data.append(data_obj)
    return data
