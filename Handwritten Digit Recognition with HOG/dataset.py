import cv2
import numpy as np
import pandas as pd
from PIL.Image import fromarray


def load_digits(file_path):
    df = pd.read_csv(file_path)
    labels = df["label"]
    return [cv2.cvtColor(np.array(fromarray(np.uint8(np.reshape(digit, (28, 28))), mode="L")), cv2.COLOR_RGB2BGR)
            for digit in df.drop(columns=['label']).values], labels
