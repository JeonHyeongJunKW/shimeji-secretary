# Copyright 2024 hd company
# Authors: Hyeongjun Jeon


import sys

# from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QComboBox, QPushButton
from PyQt5 import uic

from utility.monitor import get_monitor_info
from widget_resource.path import get_resource_path

class MainDrawer:

    def __init__(self):
        self.__app = QApplication(sys.argv)
        self.__main_window = QMainWindow()
        resource_path = get_resource_path("mainwindow.ui")
        uic.loadUi(resource_path, self.__main_window)

        self.__monitor_info = get_monitor_info()
        primary_monitor_index = self.__monitor_info['primary_index']
        monitor_width = self.__monitor_info['size'][primary_monitor_index]['width']
        x_offset = self.__monitor_info['size'][primary_monitor_index]['x_offset']
        y_offset = self.__monitor_info['size'][primary_monitor_index]['y_offset']
        origin_geometry = self.__main_window.geometry()
        self.__window_size = {'left': 0,
                            'top': 0,
                            'width': origin_geometry.width(),
                            'height': origin_geometry.height()}
        self.__window_size['left'] = monitor_width + x_offset - self.__window_size['width']
        self.__window_size['top'] = y_offset

        self.__main_window.setGeometry(
            self.__window_size['left'],
            self.__window_size['top'],
            self.__window_size['width'],
            self.__window_size['height'])

        self.__addition_button : QPushButton = self.__main_window.addition_button
        self.__addition_edit_box : QLineEdit = self.__main_window.addition_edit_box
        self.__property_combobox : QComboBox = self.__main_window.property_combobox
        self.__property_combobox.addItem("유동길")
        self.__property_combobox.addItem("default")
        last_index = self.__property_combobox.count() - 1
        self.__property_combobox.setCurrentIndex(last_index)

        self.__addition_button.clicked.connect(self.add_shimeji)

    def activate(self):
        self.__main_window.show()
        self.__app.exec_()

    def add_shimeji(self):
        shimeji_name = self.__addition_edit_box.text()

        is_valid : bool = len(shimeji_name) == 0
        if not is_valid:
            return
        self.__addition_edit_box.clear()
        target_property = self.__property_combobox.currentText()
