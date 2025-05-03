import logging
from abc import ABC

import cv2
import io
from datetime import datetime
from sklearn.cluster import KMeans
from collections import Counter
import imageio

from model.processing_model_base import ProcessingModelBase


def modify_img(image):
    modified_img = cv2.resize(image,
                              (600, 400),
                              interpolation=cv2.INTER_AREA)
    modified_img = modified_img.reshape(modified_img.shape[0] * modified_img.shape[1], 3)
    return modified_img


class ColorModel(ProcessingModelBase, ABC):
    def __init__(self):
        super().__init__()

    def process_data(self, bytes_data):
        # ToDo use only utc now
        started_time = datetime.now()
        image = imageio.imread(io.BytesIO(bytes_data), mode='L', pilmode="RGB")
        colors, values = self.get_base_colors(image, 4)
        ended_time = datetime.now()

        logging.warning(f'TIME:{ended_time - started_time}')

        # ToDo extract a class with red green blue props?
        return [{'red': color[0], 'green': color[1], 'blue': color[2]} for color in colors]

    @staticmethod
    def get_base_colors(image, number_of_colours):
        image = modify_img(image)

        clf = KMeans(n_clusters=number_of_colours)
        labels = clf.fit_predict(image)

        counts = Counter(labels)
        counts = dict(sorted(counts.items()))

        center_colours = clf.cluster_centers_
        ordered_colours = [center_colours[i] for i in counts.keys()]

        rgb_colors = [ordered_colours[i].astype(int) for i in counts.keys()]

        return rgb_colors, list(counts.values())
