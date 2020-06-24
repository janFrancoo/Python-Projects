import cv2
import numpy as np

vid_name = "vid_1.mp4"
vid = cv2.VideoCapture(vid_name)

if not vid.isOpened():
    raise Exception("Error while opening the %s" % vid_name)


def print_coordinate(event, x, y, _, __):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)


ret, frame = vid.read()
frame_shape = frame.shape
tmp_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
mask = np.zeros_like(tmp_gray)
line_image = np.copy(frame) * 0

while vid.isOpened():
    ret, frame = vid.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edge = cv2.Canny(blur, 50, 150)
        vertices = np.array([[(600, 450), (200, 700), (1200, 700), (750, 450)]],
                            dtype=np.int32)  # points are grabbed by print_coordinate func
        cv2.fillConvexPoly(mask, vertices, 255)
        masked = cv2.bitwise_and(edge, mask)
        lines = cv2.HoughLinesP(masked, 2, np.pi / 180, 180, np.array([]), 50, 100)
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 5)
            line_edges = cv2.addWeighted(frame, 0.8, line_image, 1, 0)
            cv2.imshow(vid_name, line_edges)
            if cv2.waitKey(25) and 0xFF == ord('q'):
                break
        else:
            cv2.imshow(vid_name, frame)
            if cv2.waitKey(25) and 0xFF == ord('q'):
                break
        cv2.setMouseCallback(vid_name, print_coordinate)
    else:
        break

vid.release()
cv2.destroyAllWindows()
