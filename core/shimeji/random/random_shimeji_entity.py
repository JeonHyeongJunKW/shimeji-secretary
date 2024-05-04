# Copyright 2024 Hyeongjun Jeon
# Authors: Hyeongjun Jeon

import copy
import random
import threading
import time

from core.resource_handle.state_type import SHIMEJI_ANGRY, SHIMEJI_SURPRISED
from core.resource_handle.state_type import SHIMEJI_DISAPPOINTED, SHIMEJI_SMILE
from core.shimeji.base.base_shimeji_entity import BaseEntityProperty, BaseShimejiEntity

from PyQt5.QtCore import QPoint


class RandomEntityProperty(BaseEntityProperty):

    def __init__(self, use_random_seed, **kwargs):
        super(RandomEntityProperty, self).__init__(**kwargs)
        self._entity_properties['use_random_seed'] = use_random_seed
        self.property_type = 'random'

    def check_validation(self) -> bool:
        result = super().check_validation()
        if not result:
            return False
        if 'use_random_seed' not in self._entity_properties:
            entity_name = self._entity_properties['name']
            print('There is no random seed option in {0}'.format(entity_name))
            return False
        return True


class RandomShimejiEntity(BaseShimejiEntity):

    def __init__(self, entity_property):
        super(RandomShimejiEntity, self).__init__(entity_property)
        self._use_random_seed = entity_property.get('use_random_seed')

        if self._use_random_seed:
            self._seed = 10
        random_offset = self.get_random_x()
        origin_init_pose = copy.deepcopy(self._init_pose)
        origin_init_pose.setX(random_offset)
        if self._monitor_roi.contains(origin_init_pose):
            self._init_pose = origin_init_pose
        self.__is_mouse_handling = False

    def activate(self):
        super().activate()
        self._random_move_thread = threading.Thread(target=self._move_random)
        self._random_move_thread.start()

    def _move_random(self):
        move_speed = 1  # pixel / second
        drop_speed = 3  # pixel / second
        move_timing = 0.05  # second
        change_time = 3  # second
        tracking_end_time = time.time()
        target_x = self._init_pose.x()
        normal_y = self._init_pose.y()
        while True:

            time.sleep(move_timing)

            if self._interface.isHidden():
                break

            if self.__is_mouse_handling:
                continue

            current_time = time.time()

            current_position = copy.deepcopy(self._position)
            if current_position.y() < normal_y:
                target_y = current_position.y() + drop_speed
                if target_y >= normal_y:
                    target_y = normal_y

                if target_y <= normal_y - 30:
                    self._change_shimeji_state(SHIMEJI_SURPRISED)
                else:
                    self._change_shimeji_state(SHIMEJI_SMILE)

                current_position.setY(target_y)
            else:
                change_target = tracking_end_time < current_time
                if change_target:
                    target_x = self.get_random_x()
                    tracking_end_time = current_time + change_time

                move_direction = target_x - current_position.x()
                if move_direction < 0:
                    current_position.setX(current_position.x() - move_speed)
                elif move_direction > 0:
                    current_position.setX(current_position.x() + move_speed)
                else:
                    target_x = self.get_random_x()
                    tracking_end_time = current_time + change_time
            self._set_position(current_position)

    def _process_input(self, input_data):
        event_name = input_data[0]
        mouse_handling = True
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
            mouse_handling = False
        self.__is_mouse_handling = mouse_handling

    def get_random_x(self):
        return int(random.random() * self._monitor_roi.width() + self._monitor_roi.x())
