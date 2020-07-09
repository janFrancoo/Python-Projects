import os
import cv2

labels = ["Daffodil", "Snowdrop", "Lilly Valley", "Bluebell", "Crocus", "Iris", "Tigerlily", "Tulip", "Fritillary",
          "Sunflower", "Daisy", "Colts' Foot", "Dandelion", "Cowslip", "Buttercup", "Windflower", "Pansy"]


def get_flowers(flowers_path, masks_path):
    count = -1
    masks = []
    flowers = []
    classes = []
    for i, file_name in enumerate(os.listdir(flowers_path)):
        if i % 80 == 0:
            count += 1
        raw_file_name = file_name.split(".")[0]
        file_name_for_mask = raw_file_name + ".png"
        if os.path.exists(os.path.join(masks_path, file_name_for_mask)):
            mask = cv2.imread(os.path.join(masks_path, file_name_for_mask))
            masks.append(cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY))
            flowers.append(cv2.imread(os.path.join(flowers_path, file_name)))
            classes.append(labels[count])
    return flowers, masks, classes
