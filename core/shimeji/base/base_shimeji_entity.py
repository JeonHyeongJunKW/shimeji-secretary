# Copyright 2024 hd company
# Authors: Hyeongjun Jeon

import threading

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from utility.monitor import get_monitor_info
from widget_resource.path import get_resource_path


class BaseEntityProperty:
    # animation_type
    STATIC = True
    DYNAMIC = False

    def __init__(self):
        self.entity_properties = []

    def add(self, name: str, animation_type: bool = STATIC, target_monitor: int = 0):
        self.entity_properties.append(
            {'name': name,
             'animation_type': animation_type,
             'target_monitor': target_monitor})

    @staticmethod
    def check_validation(entity: dict) -> bool:
        monitor_info = get_monitor_info()
        if 'name' not in entity:
            print('no name in ', entity)
            return False
        if 'animation_type' not in entity:
            print('There is no animation type in {0}'.format(entity['name']))
            return False
        if 'target_monitor' not in entity:
            print('There is no target monitor type in {0}'.format(entity['name']))
            return False
        if entity['target_monitor'] >= monitor_info['count']:
            print('Target monitor index {0} should be smaller than {1} in {2}'.format(
                entity['target_monitor'], monitor_info['count'], entity['name']))
            return False
        return True


class BaseShimejiEntity:

    def __init__(self, entity_property: dict):
        self._interface = QWidget()
        resource_path = get_resource_path("shimeji/base.ui")
        uic.loadUi(resource_path, self._interface)
        self._name = entity_property['name']
        self._animation_type = entity_property['animation_type']

        self._monitor_info = get_monitor_info()
        self._target_monitor_lock = threading.Lock()
        self._target_monitor = entity_property['target_monitor']

        self._position_lock = threading.Lock()
        self._position = {'x': -1, 'y': -1}

    def activate(self):
        self._interface.show()

    def set_position(self, position: dict) -> bool:
        if 'x' not in position or 'y' not in position:
            return False
        self._position_lock.acquire()
        self._position['x'] = position['x']
        self._position['y'] = position['y']
        self._position_lock.release()
        return True

    def set_monitor(self, index: int) -> bool:
        if index >= self._monitor_info['count']:
            return False
        self._target_monitor_lock.acquire()
        self._target_monitor = index
        self._target_monitor_lock.release()
        return True