# Copyright 2024 Hyeongjun Jeon
# Authors: Hyeongjun Jeon

import os

from core.shimeji.base.base_shimeji_entity import BaseEntityProperty, BaseShimejiEntity
from utility.monitor import get_monitor_info
from widget_resource.path import get_resource_path

class BaseShimejiBuilder:

    def __init__(self):
        pass

    def check_validation(self, entity_property: BaseEntityProperty) -> bool:
        monitor_info = get_monitor_info()
        if entity_property.get('name') is None:
            print('no name in property')
            return False
        name = entity_property.get('name')
        if entity_property.get('state_path') is None:
            print('There is no shimeji state_path in {0} property'.format(name))
            return False
        state_directory = entity_property.get('state_path')
        absolute_state_path = get_resource_path(state_directory)
        if not os.path.isdir(absolute_state_path):
            print('{0} does not exist'.format(state_directory))
            return False
        if entity_property.get('target_monitor') is None:
            print('There is no target monitor type in {0} property'.format(name))
            return False
        if entity_property.get('target_monitor') >= monitor_info['count']:
            print('Target monitor index {0} should be smaller than {1} in {2}'.format(
                entity_property.get('target_monitor'), monitor_info['count'], name))
            return False
        return True

    def make_entity(self, entity_property):
        is_valid = self.check_validation(entity_property)
        if not is_valid:
            return None

        return BaseShimejiEntity(entity_property)
