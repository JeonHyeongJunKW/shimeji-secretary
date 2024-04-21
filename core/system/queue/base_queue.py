# Copyright 2024 hd company
# Authors: Hyeongjun Jeon

import threading


class BaseQueue:

    def __init__(self, size) -> None:
        self._size = size
        self._queue: list = []
        self._queue_lock = threading.Lock()

    def add_queue(self, data) -> None:
        self._queue_lock.acquire()
        if self._size > len(self._queue):
            self._queue.append(data)
        self._queue_lock.release()

    def pop_queue(self):
        output_data = None
        self._queue_lock.acquire()
        if 0 < len(self._queue):
            output_data = self._queue.pop(0)
        self._queue_lock.release()
        return output_data


if __name__ == '__main__':
    test = BaseQueue(3)
    test.add_queue(3)
    test.add_queue(4)
    test.add_queue(7)
    print(test.pop_queue())
    print(test.pop_queue())
    print(test.pop_queue())
    print(test.pop_queue())
