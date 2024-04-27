# Copyright 2024 hd company
# Authors: Hyeongjun Jeon

import os

from PyQt5 import uic, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QLabel, QWidget

from core.resource_handle.state_type import *
from core.resource_handle.resource_interface import load_static_shimeji_state, get_shimeji_state
from widget_resource.path import get_resource_path

class ShimejiInterface(QWidget):

    def __init__(self, resource_path: str, dir_path: str):
        super().__init__()
        uic.loadUi(get_resource_path(resource_path), self)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.__name_label: QLabel = self.name_label
        self.__state_interface: QLabel = self.image_label

        self.__name_label.setStyleSheet(
            'color: black;'
            'background-color: #FA8072')

        self.__current_state: str = ""
        self.__state_type = []
        self.__state_namespace = dir_path.split('/')[-1] + '_'

        state_directory = get_resource_path(dir_path)
        state_file_list: list = os.listdir(state_directory)
        state_files = []

        for state_file_name in state_file_list:
            self.__state_type.append(self.__state_namespace + state_file_name.split('.')[0])
            state_files.append(os.path.join(state_directory, state_file_name))

        opacity_effect = QGraphicsOpacityEffect(self)
        opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(opacity_effect)

        load_static_shimeji_state(self.__state_type, state_files, self.__state_interface.size())

        self.change_shimeji_state(SHIMEJI_DEFAULT)

    def set_name(self, name: str):
        self.__name_label.setText(name)

    def change_shimeji_state(self, state_type):
        if self.__current_state == state_type:
            return
        self.__current_state = state_type
        target_image: QtGui.QPixmap = get_shimeji_state(self.__state_namespace + state_type)

        if target_image is not None:
            self.__state_interface.setPixmap(target_image)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
            self.change_shimeji_state(SHIMEJI_ANGRY)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
            self.change_shimeji_state(SHIMEJI_DISAPPOINTED)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)
        self.change_shimeji_state(SHIMEJI_SMILE)

