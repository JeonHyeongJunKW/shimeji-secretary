# Copyright 2024 Hyeongjun Jeon
# Authors: Hyeongjun Jeon

import os
import sys

from core.drawer.entity.shimeji_interface import ShimejiInterface
from core.shimeji.base.base_shimeji_entity import BaseEntityProperty
from core.shimeji.random.random_shimeji_entity import RandomEntityProperty
from core.system.queue.call_queue import CallQueue

from PyQt5 import uic
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QApplication, QComboBox, QLineEdit
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QPushButton
from utility.monitor import get_monitor_info
from widget_resource.path import get_resource_path


class MainDrawer(QMainWindow):

    def __init__(self, shimeji_generation_queue: CallQueue):
        self.__app = QApplication(sys.argv)
        super().__init__()
        resource_path = get_resource_path('mainwindow.ui')
        uic.loadUi(resource_path, self)

        self.__monitor_info = get_monitor_info()

        RANDOM = 'random'
        DEFAULT = 'default'
        self.shimeji_generation_queue = shimeji_generation_queue

        self.primary_monitor_index = self.__monitor_info['primary_index']
        monitor_width = self.__monitor_info['size'][self.primary_monitor_index]['width']
        x_offset = self.__monitor_info['size'][self.primary_monitor_index]['x_offset']
        y_offset = self.__monitor_info['size'][self.primary_monitor_index]['y_offset']
        origin_geometry = self.geometry()
        self.__window_size = \
            {'left': 0,
             'top': 0,
             'width': origin_geometry.width(),
             'height': origin_geometry.height()}
        self.__window_size['left'] = monitor_width + x_offset - self.__window_size['width']
        self.__window_size['top'] = y_offset

        self.setGeometry(
            self.__window_size['left'],
            self.__window_size['top'],
            self.__window_size['width'],
            self.__window_size['height'])

        self.__addition_button: QPushButton = self.addition_button
        self.__removal_button: QPushButton = self.removal_button
        self.__addition_edit_box: QLineEdit = self.addition_edit_box

        self.__property_combobox: QComboBox = self.property_combobox
        self.__property_combobox.addItem(RANDOM, RandomEntityProperty)
        self.__property_combobox.addItem(DEFAULT, BaseEntityProperty)
        self.__removal_combobox: QComboBox = self.removal_combobox

        default_index = self.__property_combobox.findText(DEFAULT)
        self.__property_combobox.setCurrentIndex(default_index)

        self.__addition_button.clicked.connect(self.__add_shimeji)
        self.__removal_button.clicked.connect(self.__remove_shimeji)

        self.__shimeji_interface_set = []

    def activate(self):
        self.show()
        self.__app.exec_()

    def __remove_shimeji(self):
        target_shimeji_name = self.__removal_combobox.currentText()
        target_shimeji_index = self.__removal_combobox.currentIndex()
        if target_shimeji_index == -1:
            return

        for shimeji_interface in self.__shimeji_interface_set:
            target_interface: ShimejiInterface = shimeji_interface
            if target_interface.get_name() == target_shimeji_name:
                target_interface.hide()
                break
        self.__removal_combobox.removeItem(target_shimeji_index)

    def __add_shimeji(self):
        shimeji_name = self.__addition_edit_box.text()
        if len(shimeji_name) == 0:
            QMessageBox.warning(self, 'Warn', '너무 이름이 짧아요.')
            return
        elif self.__removal_combobox.findText(shimeji_name) != -1:
            QMessageBox.warning(self, 'Warn', '이미 같은 이름으로 존재합니다.')
            return

        target_property = self.__property_combobox.currentData()
        resource_path = 'shimeji/base.ui'
        state_directory = 'shimeji/emoji_state'

        shimeji_interface = ShimejiInterface(resource_path, state_directory)
        self.__shimeji_interface_set.append(shimeji_interface)

        entity_property = None
        if target_property == RandomEntityProperty:
            entity_property = \
                RandomEntityProperty(
                    use_random_seed=False,
                    name=shimeji_name,
                    interface=self.__shimeji_interface_set[-1],
                    target_monitor=self.primary_monitor_index)
        else:
            entity_property = \
                BaseEntityProperty(
                    name=shimeji_name,
                    interface=self.__shimeji_interface_set[-1],
                    target_monitor=self.primary_monitor_index)
        self.shimeji_generation_queue.add_queue(entity_property)
        self.__removal_combobox.addItem(shimeji_name)

    def closeEvent(self, event: QCloseEvent):
        for shimeji_interface in self.__shimeji_interface_set:
            target_interface: ShimejiInterface = shimeji_interface
            target_interface.hide()
        event.accept()
