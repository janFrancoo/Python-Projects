import cv2
import numpy as np


def get_hash(image, size=8):
    resized = cv2.resize(image, (size + 1, size))
    diff = resized[:, 1:] > resized[:, :-1]
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


def convert_hash(h):
    return int(np.array(h, dtype="float64"))


def hamming(h_a, h_b):
    return bin(int(h_a) ^ int(h_b)).count("1")
