import cv2


class FeatureExtract:
    def __init__(self, image):
        self.image = image
        self.sift = cv2.xfeatures2d.SIFT_create()

    def extract_features(self):
        kp, des = self.sift.detectAndCompute(self.image, None)
        return kp, des
