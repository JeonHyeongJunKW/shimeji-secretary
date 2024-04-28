# Copyright 2024 hd company
# Authors: Hyeongjun Jeon

import os

from core.system.queue.call_queue import CallQueue

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QLabel, QWidget
from widget_resource.path import get_resource_path


class ShimejiInterface(QWidget):

    def __init__(self, resource_path: str, dir_path: str):
        super().__init__()
        uic.loadUi(get_resource_path(resource_path), self)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        opacity_effect = QGraphicsOpacityEffect(self)
        opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(opacity_effect)

        self.__name_label: QLabel = self.name_label
        self.state_interface: QLabel = self.image_label

        self.__name_label.setStyleSheet('color: black;''background-color: #FA8072')

        self.state_type = []
        self.unique_state_type = []
        self.state_files = []
        self.state_namespace = dir_path.split('/')[-1] + '_'

        state_directory = get_resource_path(dir_path)
        state_file_list: list = os.listdir(state_directory)

        for state_file_name in state_file_list:
            self.state_type.append(state_file_name.split('.')[0])
            self.unique_state_type.append(self.state_namespace + self.state_type[-1])
            self.state_files.append(os.path.join(state_directory, state_file_name))

        self.__interface_queue: CallQueue = CallQueue(size=100)

    def set_name(self, name: str):
        self.__name_label.setText(name)

    def get_interface_queue(self):
        return self.__interface_queue

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            point_info = [event.x(), event.y(), event.globalX(), event.globalY()]
            self.__interface_queue.add_queue(['left_press', point_info])

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            point_info = [event.x(), event.y(), event.globalX(), event.globalY()]
            self.__interface_queue.add_queue(['left_move', point_info])

    def mouseReleaseEvent(self, event):
        point_info = [event.x(), event.y(), event.globalX(), event.globalY()]
        self.__interface_queue.add_queue(['release', point_info])
