import cv2
import numpy as np

lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
             'v', 'w', 'x', 'y', 'z']
uppercase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
             'V', 'W', 'X', 'Y', 'Z']


def generate_rgb():
    r = np.random.randint(0, 255)
    g = np.random.randint(0, 255)
    b = np.random.randint(0, 255)
    return r, g, b


def create_captcha(generate=1, size=5, color=0):
    for captcha in range(generate):
        white_bg = np.ones((50, 150, 3)) * 255
        white_bg = white_bg.astype('uint8')
        pos_x = 0
        pos_y = 30
        real = ""
        for i in range(size):
            char = np.random.randint(0, 3)
            if char == 0:
                num = np.random.randint(0, 10)
                thickness = np.random.randint(2, 7)
                if color:
                    cv2.putText(white_bg, str(num), (pos_x, pos_y), cv2.FONT_HERSHEY_SIMPLEX, 1, generate_rgb(),
                                thickness)
                else:
                    cv2.putText(white_bg, str(num), (pos_x, pos_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), thickness)
                real += str(num)
            if char == 1:
                num = np.random.randint(0, 26)
                thickness = np.random.randint(2, 7)
                if color:
                    cv2.putText(white_bg, lowercase[num], (pos_x, pos_y), cv2.FONT_HERSHEY_SIMPLEX, 1, generate_rgb(),
                                thickness)
                else:
                    cv2.putText(white_bg, lowercase[num], (pos_x, pos_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),
                                thickness)
                real += lowercase[num]
            if char == 2:
                num = np.random.randint(0, 26)
                thickness = np.random.randint(2, 7)
                if color:
                    cv2.putText(white_bg, uppercase[num], (pos_x, pos_y), cv2.FONT_HERSHEY_SIMPLEX, 1, generate_rgb(),
                                thickness)
                else:
                    cv2.putText(white_bg, uppercase[num], (pos_x, pos_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),
                                thickness)
                real += uppercase[num]
            pos_x += int(150 / size)
        for i in range(size * 2):
            line_pos_x1 = np.random.randint(0, 150)
            line_pos_x2 = np.random.randint(0, 150)
            line_pos_y1 = np.random.randint(0, 50)
            line_pos_y2 = np.random.randint(0, 50)
            increment1 = np.random.randint(0, 50)
            increment2 = np.random.randint(0, 50)
            if color:
                cv2.line(white_bg, (line_pos_x1, line_pos_x2), (line_pos_y1 + increment1, line_pos_y2 + increment2),
                         generate_rgb(), 2)
            else:
                cv2.line(white_bg, (line_pos_x1, line_pos_x2), (line_pos_y1 + increment1, line_pos_y2 + increment2),
                         (0, 0, 0), 2)
        print(real)
        cv2.imshow('white', white_bg)
        cv2.waitKey(0)


create_captcha(10, 7, 1)
