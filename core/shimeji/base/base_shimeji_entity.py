# Copyright 2024 Hyeongjun Jeon
# Authors: Hyeongjun Jeon

import copy
import threading

from core.drawer.entity.shimeji_interface import ShimejiInterface
from core.resource_handle.resource_interface import get_shimeji_state, load_static_shimeji_state
from core.resource_handle.state_type import SHIMEJI_ANGRY, SHIMEJI_DEFAULT
from core.resource_handle.state_type import SHIMEJI_DISAPPOINTED, SHIMEJI_SMILE
from core.system.queue.call_queue import CallQueue
from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, QRect
from utility.monitor import get_monitor_info


class BaseEntityProperty:

    def __init__(self, name, interface, target_monitor):
        self._entity_properties = \
            {'name': name,
             'interface': interface,
             'target_monitor': target_monitor}
        self.property_type = 'base'

    def get(self, name: str):
        if name in self._entity_properties:
            return self._entity_properties[name]
        else:
            return None


class BaseShimejiEntity:

    def __init__(self, entity_property: BaseEntityProperty):
        self._name = entity_property.get('name')
        self._interface: ShimejiInterface = entity_property.get('interface')
        self.__interface_queue: CallQueue = self._interface.get_interface_queue()

        self._monitor_info = get_monitor_info()
        self._target_monitor_lock = threading.Lock()
        self._target_monitor_index = entity_property.get('target_monitor')
        self._current_monitor_size = self._monitor_info['size'][self._target_monitor_index]

        self._position_lock = threading.Lock()
        init_x = \
            self._current_monitor_size['x_offset'] + \
            self._current_monitor_size['width'] / 2 - \
            self._interface.size().width() / 2 - 1
        init_y = \
            self._current_monitor_size['y_offset'] + \
            self._current_monitor_size['height'] - \
            self._interface.size().height() - 1
        self._init_pose = QPoint(init_x, init_y)
        self._monitor_roi = \
            QRect(
                self._current_monitor_size['x_offset'],
                self._current_monitor_size['y_offset'],
                self._current_monitor_size['width'] - self._interface.size().width(),
                self._current_monitor_size['height'] - self._interface.size().height())
        self._position: QPoint = copy.deepcopy(self._init_pose)
        self._mouse_click_point = \
            QPoint(self._interface.size().width() / 2, self._interface.size().height() / 2)

        self.__current_state: str = ''

    def _init_shimeji(self):
        load_static_shimeji_state(
            self._interface.unique_state_type,
            self._interface.state_files,
            self._interface.state_interface.size())

        self._change_shimeji_state(SHIMEJI_DEFAULT)

    def get_name(self):
        return self._name

    def activate(self):
        self._init_shimeji()
        self._interface.show()
        self._reaction_thread = threading.Thread(target=self.__react_to_input)
        self._reaction_thread.start()
        self._set_position(self._init_pose)

    def deactivate(self):
        self._interface.hide()
        self._reaction_thread.join()

    def close(self):
        self._interface.close()

    def _process_input(self, input_data):
        event_name = input_data[0]
        if event_name == 'left_press':
            self._change_shimeji_state(SHIMEJI_ANGRY)
            self._mouse_click_point = QPoint(input_data[1][0], input_data[1][0])
        elif event_name == 'left_move':
            self._change_shimeji_state(SHIMEJI_DISAPPOINTED)
            mouse_move_point: QPoint = QPoint(input_data[1][2], input_data[1][3])
            target_point = mouse_move_point - self._mouse_click_point
            self._set_position(target_point)
        elif event_name == 'release':
            self._change_shimeji_state(SHIMEJI_SMILE)
            mouse_move_point: QPoint = QPoint(input_data[1][2], input_data[1][3])
            target_point = mouse_move_point - self._mouse_click_point
            target_point.setY(self._monitor_roi.height() - 1)
            self._set_position(target_point)

    def _change_shimeji_state(self, state_type):
        if self.__current_state == state_type:
            return
        self.__current_state = state_type
        target_image: QtGui.QPixmap = \
            get_shimeji_state(self._interface.state_namespace + self.__current_state)

        if target_image is not None:
            self._interface.state_interface.setPixmap(target_image)

    def _set_position(self, position: QPoint):
        if self._monitor_roi.contains(position):
            with self._position_lock:
                self._position = position
                self._interface.move(self._position)

    def _set_monitor(self, index: int) -> bool:
        if index >= self._monitor_info['count']:
            return False
        with self._target_monitor_lock:
            self._target_monitor = index
        return True

    def __react_to_input(self):
        input_call = self.__interface_queue.get_queue_call()
        queue = self.__interface_queue
        while True:
            with input_call:
                input_call.wait(timeout=0.1)

            if self._interface.isHidden():
                break

            current_queue_size = queue.get_queue_size()

            for _ in range(current_queue_size):
                input_data: dict = queue.pop_queue()
                self._process_input(input_data)
