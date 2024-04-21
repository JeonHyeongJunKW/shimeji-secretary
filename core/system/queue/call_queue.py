# Copyright 2024 hd company
# Authors: Hyeongjun Jeon

from threading import Condition

from core.system.queue.base_queue import BaseQueue

class CallQueue(BaseQueue):

    def __init__(self, size) -> None:
        super().__init__(size)
        self.call = Condition()

    def get_queue_call(self):
        return self.call

    def add_queue(self, data) -> None:
        super().add_queue(data)
        with self.call:
            self.call.notify_all()

    def get_queue_size(self) -> int:
        with self._queue_lock:
            return len(self._queue)


if __name__ == '__main__':
    import threading
    import time

    def add_data(queue : CallQueue):
        i : int = 0
        while i <= 50:
            print('Success to add', i)
            queue.add_queue(i)
            i += 1

    def read_data(queue : CallQueue):
        call = queue.get_queue_call()
        data = 0
        while data < 50:
            with call:
                call.wait(timeout=0.1)  # wait for check size
            current_queue_size = queue.get_queue_size()

            for _ in range(current_queue_size):
                data = queue.pop_queue()
                print('Success to pop', data)

    call_queue = CallQueue(3)
    read_thread = threading.Thread(target=add_data, args=(call_queue,))
    add_thread = threading.Thread(target=read_data, args=(call_queue,))

    read_thread.start()
    add_thread.start()
