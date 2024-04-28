# Copyright 2024 hd company
# Authors: Hyeongjun Jeon

import threading

from core.drawer.main_drawer import MainDrawer
from core.shimeji.base.base_shimeji_builder import BaseShimejiBuilder
from core.shimeji.random.random_shimeji_builder import RandomShimejiBuilder
from core.system.queue.call_queue import CallQueue


class ShimejiSecretarySystem:

    def __init__(self):
        print('=========시메지 월드=========')
        self.shimeji_generation_queue = CallQueue(size=10)
        self.shimeji_generation_thread = threading.Thread(target=self.make_shimeji)
        self.shimeji_generation_thread.start()
        self.main_window_closed = False
        self.__main_drawer = MainDrawer(self.shimeji_generation_queue)
        self.shimeji_set = []

    def activate(self):
        self.__main_drawer.activate()
        self.main_window_closed = True
        self.shimeji_generation_thread.join()
        for shimeji in self.shimeji_set:
            shimeji.deactivate()
        self.shimeji_set.clear()

    def make_shimeji(self):
        generation_call = self.shimeji_generation_queue.get_queue_call()
        queue = self.shimeji_generation_queue
        base_builder = BaseShimejiBuilder()
        random_builder = RandomShimejiBuilder()
        while True:
            with generation_call:
                generation_call.wait(timeout=0.1)

            if self.main_window_closed:
                break

            current_queue_size = queue.get_queue_size()

            for _ in range(current_queue_size):
                shimeji_property = queue.pop_queue()
                if shimeji_property.property_type == 'random':
                    entity = random_builder.make_entity(shimeji_property)
                else:
                    entity = base_builder.make_entity(shimeji_property)

                if entity is not None:
                    self.shimeji_set.append(entity)
                    entity.activate()
