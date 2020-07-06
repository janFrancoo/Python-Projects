class FaceDetector:
    def __init__(self, cascade):
        self.cascade = cascade

    def detect_faces(self, img, scale_factor, min_neighbors):
        rects = self.cascade.detectMultiScale(img, scaleFactor=scale_factor, minNeighbors=min_neighbors,
                                              minSize=(70, 70))
        return rects
