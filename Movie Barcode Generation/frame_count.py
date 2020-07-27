import cv2


def get_frame_count(video_path, mode="ideal"):
    total_frames = 0
    vid = cv2.VideoCapture(video_path)

    if mode == "slower":
        while True:
            grabbed, _ = vid.read()
            if not grabbed:
                break
            total_frames += 1
    elif mode == "ideal":
        try:
            total_frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
        except:
            while True:
                grabbed, _ = vid.read()
                if not grabbed:
                    break
                total_frames += 1
    else:
        total_frames = -1

    vid.release()
    return total_frames
