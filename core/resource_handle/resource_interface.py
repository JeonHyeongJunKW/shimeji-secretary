# Copyright 2024 hd company
# Authors: Hyeongjun Jeon

import copy

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize

from core.resource_handle.resource_server import ResourceServer

def load_static_shimeji_state(resource_names: list, resource_paths: list, image_size: QSize):

    def load_pixmap(resource_path, size: QSize=image_size):
        pixmap = QtGui.QPixmap(resource_path)
        pixmap = pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return pixmap

    for i in range(len(resource_names)):
        ResourceServer.load_resource(resource_names[i], resource_paths[i], load_pixmap)

def load_dynamic_shimeji_state(resource_names: list, resource_paths: list):

    def load_pixmap(resource_path):
        return QtGui.QPixmap(resource_path)

    for i in range(len(resource_names)):
        ResourceServer.load_resource(resource_names[i], resource_paths[i], load_pixmap)

def get_shimeji_state(state_name: str):
    success, resource = ResourceServer.get_resource(state_name)
    if success:
        return resource
    else :
        print('Failed to get {} state'.format(state_name))
        return None
