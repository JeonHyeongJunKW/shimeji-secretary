# Copyright 2024 Hyeongjun Jeon
# Authors: Hyeongjun Jeon

import threading
import time

from core.resource_handle.image_handle.resource_interface \
    import get_shimeji_state, load_dynamic_shimeji_state
from core.resource_handle.state_type import SHIMEJI_DEFAULT
from core.shimeji.random.random_shimeji_entity import RandomEntityProperty, RandomShimejiEntity

from PyQt5 import QtGui


class DynamicEntityProperty(RandomEntityProperty):

    def __init__(self, **kwargs):
        super(DynamicEntityProperty, self).__init__(**kwargs)
        self.property_type = 'dynamic'


class DynamicShimejiEntity(RandomShimejiEntity):

    def __init__(self, entity_property):
        super(DynamicShimejiEntity, self).__init__(entity_property)
        self._current_dynamic_image_set = []

    def activate(self):
        super().activate()
        self._dynamic_move_thread = threading.Thread(target=self.__play_dynamic_action)
        self._dynamic_move_thread.start()

    def deactivate(self):
        super().deactivate()

    def _process_input(self, input_data):
        super()._process_input(input_data)

    def _init_shimeji(self):
        load_dynamic_shimeji_state(
            self._interface.unique_state_type,
            self._interface.state_files,
            self._interface.state_interface.size())

        self._change_shimeji_state(SHIMEJI_DEFAULT)

    def _change_shimeji_state(self, state_type):
        if self._current_state == state_type:
            return
        with self._status_lock:
            self._current_state = state_type

    def __play_dynamic_action(self):
        act_timing = 0.1  # second
        last_status = ''
        current_step = 0
        max_action_step = 0
        while True:
            time.sleep(act_timing)

            if self._interface.isHidden():
                break

            if last_status != self._current_state:
                last_status = self._current_state
                with self._status_lock:
                    self._current_dynamic_image_set = \
                        get_shimeji_state(self._interface.state_namespace + self._current_state)
                    max_action_step = len(self._current_dynamic_image_set)
                    current_step = 0

            if last_status == '':
                continue

            if max_action_step == 0:
                continue

            target_pixmap: QtGui.QPixmap = self._current_dynamic_image_set[current_step]
            if self._current_direction == 1:
                target_pixmap = target_pixmap.transformed(QtGui.QTransform().scale(-1, 1))
            current_step = (current_step + 1) % max_action_step

            self._interface.state_interface.setPixmap(target_pixmap)
