# Copyright 2024 Hyeongjun Jeon
# Authors: Hyeongjun Jeon

from core.resource_handle.resource_server import ResourceServer

import cv2

from PyQt5 import QtGui
from PyQt5.QtCore import QSize, Qt


def add_alpha_channel(image: QtGui.QImage):
    size: QSize = image.size()
    h = size.height()
    w = size.width()
    for i in range(h):
        for j in range(w):
            color: QtGui.QColor = image.pixelColor(j, i)
            if color.valueF() == 1.0:
                color.setAlpha(0)
                image.setPixelColor(j, i, color)


def convert_image_to_frame(image):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
    height, width, channel = image.shape
    data_step = channel * width
    output_q_image = \
        QtGui.QImage(image.data, width, height, data_step, QtGui.QImage.Format_ARGB32)
    return output_q_image


def load_static_shimeji_state(resource_names: list, resource_paths: list, image_size: QSize):

    def load_pixmap(resource_info: list):
        resource_path: str = resource_info[0]
        target_size: QSize = resource_info[1]
        pixmap = QtGui.QPixmap(resource_path)
        pixmap = pixmap.scaled(target_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return pixmap

    for i in range(len(resource_names)):
        ResourceServer.load_resource(
            resource_names[i],
            [resource_paths[i], image_size],
            load_pixmap)


def load_dynamic_shimeji_state(resource_names: list, resource_paths: list, gif_size: QSize):

    def load_gif(resource_info: list):
        resource_path: str = resource_info[0]
        target_size: QSize = resource_info[1]
        gif = cv2.VideoCapture(resource_path)
        ret, frame = gif.read()
        frame_set = []
        while ret:
            output_image = convert_image_to_frame(frame)
            add_alpha_channel(output_image)
            output_pixmap = QtGui.QPixmap(output_image)
            output_pixmap = \
                output_pixmap.scaled(target_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            frame_set.append(output_pixmap)
            ret, frame = gif.read()
        return frame_set

    for i in range(len(resource_names)):
        ResourceServer.load_resource(resource_names[i], [resource_paths[i], gif_size], load_gif)


def get_shimeji_state(state_name: str):
    success, resource = ResourceServer.get_resource(state_name)
    if success:
        return resource
    else:
        print('Failed to get {} state'.format(state_name))
        return None
