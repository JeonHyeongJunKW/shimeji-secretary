# Copyright 2024 Hyeongjun Jeon
# Authors: Hyeongjun Jeon
import cv2

from core.resource_handle.resource_server import ResourceServer
from PyQt5 import QtGui
from PyQt5.QtCore import QSize, Qt


def convert_image_to_frame(image, convert_rgb = True):
    height, width, _ = image.shape
    data_step = 3 * width
    output_q_image = \
        QtGui.QImage(image.data, width, height, data_step, QtGui.QImage.Format_RGB888)
    if convert_rgb:
        output_q_image = output_q_image.rgbSwapped()
    return QtGui.QPixmap(output_q_image)

def load_static_shimeji_state(resource_names: list, resource_paths: list, image_size: QSize):

    def load_pixmap(resource_path, size: QSize = image_size):
        pixmap = QtGui.QPixmap(resource_path)
        pixmap = pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return pixmap

    for i in range(len(resource_names)):
        ResourceServer.load_resource(resource_names[i], resource_paths[i], load_pixmap)


def load_dynamic_shimeji_state(
    resource_names: list,
    resource_paths: list,
    movie_size: QSize):

    def load_movie(resource_path, size: QSize = movie_size):
        gif = cv2.VideoCapture(resource_path)
        ret, frame = gif.read()
        frame_set = []
        while ret:
            output_pixmap = convert_image_to_frame(frame)
            output_pixmap = output_pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            frame_set.append(output_pixmap)
            ret, frame = gif.read()
        return frame_set

    for i in range(len(resource_names)):
        ResourceServer.load_resource(resource_names[i], resource_paths[i], load_movie)


def get_shimeji_state(state_name: str):
    success, resource = ResourceServer.get_resource(state_name)
    if success:
        return resource
    else:
        print('Failed to get {} state'.format(state_name))
        return None
