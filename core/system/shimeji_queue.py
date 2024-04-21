# Copyright 2024 hd company
# Authors: Hyeongjun Jeon

import threading


class BaseQueue:

    def __init__(self, size) -> None:
        self._size = size
        self._queue : list
        self._queue_lock = threading.Lock()

    def add_queue(self, data) -> None:
        self._queue_lock.acquire()
        self._queue.append(data)
        self._queue_lock.release()

    def pop_queue(self):
        self._queue_lock.acquire()
        output_data = self._queue.pop(0)
        self._queue_lock.release()
        return output_data

class CallQueue(BaseQueue):

    def __init__(self, size) -> None:
        super().__init__(size)
