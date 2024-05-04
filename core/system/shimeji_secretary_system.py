# Copyright 2024 Hyeongjun Jeon
# Authors: Hyeongjun Jeon

import sys
import threading

from core.drawer.main_drawer import MainDrawer
from core.shimeji.base.base_shimeji_builder import BaseShimejiBuilder
from core.shimeji.base.base_shimeji_entity import BaseEntityProperty, BaseShimejiEntity
from core.shimeji.random.random_shimeji_builder import RandomShimejiBuilder
from core.system.queue.call_queue import CallQueue

from PyQt5.QtWidgets import QApplication


class ShimejiSecretarySystem:

    def __init__(self):
        print('=========시메지 월드=========')
        self.__app: QApplication = QApplication(sys.argv)
        self.shimeji_command_queue = CallQueue(size=10)
        self.shimeji_command_thread = threading.Thread(target=self.__process_command)
        self.shimeji_command_thread.start()
        self.__main_drawer = MainDrawer(self.shimeji_command_queue)
        self.shimeji_set = []

    def activate(self):
        self.__main_drawer.activate()
        self.__app.exec_()
        if self.shimeji_command_thread.is_alive():
            self.shimeji_command_thread.join()

    def __kill_shimeji(self, shimeji: BaseShimejiEntity):
        shimeji.deactivate()
        shimeji.close()
        del shimeji

    def __process_command(self):
        command_call = self.shimeji_command_queue.get_queue_call()
        queue = self.shimeji_command_queue
        base_builder = BaseShimejiBuilder()
        random_builder = RandomShimejiBuilder()
        while True:
            with command_call:
                command_call.wait(timeout=0.1)

            current_queue_size = queue.get_queue_size()
            for _ in range(current_queue_size):
                command = queue.pop_queue()
                command_type = command[0]
                if command_type == 'close':
                    for shimeji in self.shimeji_set:
                        self.__kill_shimeji(shimeji)
                    return
                elif command_type == 'removal':
                    target_name = command[1]
                    for shimeji in self.shimeji_set:
                        if target_name == shimeji.get_name():
                            self.__kill_shimeji(shimeji)
                            break
                elif command_type == 'generation':
                    shimeji_property: BaseEntityProperty = command[1]
                    if shimeji_property.property_type == 'random':
                        entity = random_builder.make_entity(shimeji_property)
                    else:
                        entity = base_builder.make_entity(shimeji_property)

                    if entity is not None:
                        self.shimeji_set.append(entity)
                        entity.activate()
