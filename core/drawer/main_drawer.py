# Copyright 2024 Hyeongjun Jeon
# Authors: Hyeongjun Jeon

from core.drawer.entity.shimeji_interface import ShimejiInterface
from core.shimeji.base.base_shimeji_entity import BaseEntityProperty
from core.shimeji.random.random_shimeji_entity import RandomEntityProperty
from core.system.queue.call_queue import CallQueue

from PyQt5 import uic
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QComboBox, QLineEdit
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QPushButton
from utility.monitor import get_monitor_info
from widget_resource.path import get_resource_path


class MainDrawer(QMainWindow):

    def __init__(self, shimeji_command_queue: CallQueue):
        super().__init__()
        resource_path = get_resource_path('mainwindow.ui')
        uic.loadUi(resource_path, self)

        self.__monitor_info = get_monitor_info()

        RANDOM = 'random'
        DEFAULT = 'default'
        self.shimeji_command_queue = shimeji_command_queue
        self._interface_set = []

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

    def activate(self):
        self.show()

    def __remove_shimeji(self):
        target_shimeji_name = self.__removal_combobox.currentText()
        target_shimeji_index = self.__removal_combobox.currentIndex()
        if target_shimeji_index == -1:
            return
        del self._interface_set[target_shimeji_index]

        self.shimeji_command_queue.add_queue(['removal', target_shimeji_name])

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

        shimeji_resource_path = 'shimeji/emoji_state'
        entity_interface =  ShimejiInterface(shimeji_name, shimeji_resource_path)
        self._interface_set.append(entity_interface)

        entity_property = None
        if target_property == RandomEntityProperty:
            entity_property = \
                RandomEntityProperty(
                    use_random_seed=False,
                    name=shimeji_name,
                    interface=entity_interface,
                    target_monitor=self.primary_monitor_index)
        else:
            entity_property = \
                BaseEntityProperty(
                    name=shimeji_name,
                    interface=entity_interface,
                    target_monitor=self.primary_monitor_index)

        self.shimeji_command_queue.add_queue(['generation', entity_property])
        self.__removal_combobox.addItem(shimeji_name)

    def closeEvent(self, event: QCloseEvent):
        self.shimeji_command_queue.add_queue(['close'])
        event.accept()
