import cv2


def get_hash(image, size=8):
    resized = cv2.resize(image, (size + 1, size))
    diff = resized[:, 1:] > resized[:, :-1]
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
