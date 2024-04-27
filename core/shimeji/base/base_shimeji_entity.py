# Copyright 2024 hd company
# Authors: Hyeongjun Jeon

import threading

from utility.monitor import get_monitor_info
from core.drawer.entity.shimeji_interface import ShimejiInterface


class BaseEntityProperty:
    # animation_type
    STATIC = True
    DYNAMIC = False

    def __init__(
            self,
            name: str,
            interface: ShimejiInterface,
            animation_type: bool = STATIC,
            target_monitor: int = 0):

        interface.set_name(name)
        self._entity_properties = \
            {'name': name,
             'interface': interface,
             'animation_type': animation_type,
             'target_monitor': target_monitor,
             'target_monitor': target_monitor}


    def get(self, name: str):
        if name in self._entity_properties:
            return self._entity_properties[name]
        else:
            return None

    def check_validation(self) -> bool:
        monitor_info = get_monitor_info()
        if 'name' not in self._entity_properties:
            print('no name in ', self._entity_properties)
            return False
        name = self._entity_properties['name']
        if 'interface' not in self._entity_properties:
            print('There is no shimeji interface in {0}'.format(name))
            return False
        if 'animation_type' not in self._entity_properties:
            print('There is no animation type in {0}'.format(name))
            return False
        if 'target_monitor' not in self._entity_properties:
            print('There is no target monitor type in {0}'.format(name))
            return False
        if self._entity_properties['target_monitor'] >= monitor_info['count']:
            print('Target monitor index {0} should be smaller than {1} in {2}'.format(
                self._entity_properties['target_monitor'], monitor_info['count'], name))
            return False
        return True


class BaseShimejiEntity:

    def __init__(self, entity_property: BaseEntityProperty):
        self._name = entity_property.get('name')
        self._animation_type = entity_property.get('animation_type')
        self._interface = entity_property.get('interface')

        self._monitor_info = get_monitor_info()
        self._target_monitor_lock = threading.Lock()
        self._target_monitor = entity_property.get('target_monitor')

        self._position_lock = threading.Lock()
        self._position = {'x': -1, 'y': -1}

    def activate(self):
        self._interface.show()

    def deactivate(self):
        self._interface.close()

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
