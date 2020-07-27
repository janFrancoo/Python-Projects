import cv2
import argparse
import numpy as np
from frame_count import get_frame_count

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True, help="Path of the video")
ap.add_argument("-s", "--save", required=True, help="Path of the barcode that will be saved")
ap.add_argument("-w", "--width", help="Width of the barcode")
ap.add_argument("-l", "--height", help="Height of the barcode")
ap.add_argument("-n", "--n_section", help="Section count")
args = vars(ap.parse_args())

n_section = 50 if args["n_section"] is None else int(args["n_section"])
width = 700 if args["width"] is None else int(args["width"])
height = 300 if args["height"] is None else int(args["height"])
vid = cv2.VideoCapture(args["video"])

frame_count = int(get_frame_count(args["video"]))
section_width = width // n_section
step = frame_count // n_section

rgb_sections = []
for i_frame in range(1, frame_count, step):
    vid.set(1, i_frame - 1)
    grabbed, frame = vid.read()

    if grabbed:
        avg_rgb = cv2.mean(frame)[:3]
        rgb_sections.append(avg_rgb)

sections = []
for (b, g, r) in rgb_sections:
    section = np.zeros([height, section_width, 3]).astype("uint8")
    section[:, :, 0] = int(b)
    section[:, :, 1] = int(g)
    section[:, :, 2] = int(r)
    sections.append(section)

barcode = np.hstack(sections)
cv2.imwrite(args["save"], barcode)
vid.release()
