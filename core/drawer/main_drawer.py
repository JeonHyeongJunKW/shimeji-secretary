# Copyright 2024 hd company
# Authors: Hyeongjun Jeon


import sys

# from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
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

        self.__main_window.addition_button.clicked.connect(self.add_shimeji)

    def activate(self):
        self.__main_window.show()
        self.__app.exec_()

    def add_shimeji(self):
        edit_box : QLineEdit = self.__main_window.addition_editbox
        text = edit_box.text()
        if len(text) != 0:
            print(text)
            edit_box.clear()
