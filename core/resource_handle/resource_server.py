# Copyright 2024 hd company
# Authors: Hyeongjun Jeon

import threading
from typing import Callable


class ResourceServer:
    global resource_data, resource_lock
    resource_data = {}
    resource_lock = threading.Lock()

    def __init__(self):
        pass

    def load_resource(resource_name: str, resource_path: str, load_method: Callable):
        is_exist: bool = ResourceServer.check_resource(resource_name)
        if not is_exist:
            with resource_lock:
                resource_data[resource_name] = load_method(resource_path)

    def get_resource(resource_name: str):
        is_exist: bool = ResourceServer.check_resource(resource_name)

        if is_exist:
            return True, resource_data[resource_name]
        else:
            return False, None

    def check_resource(resource_name: str):
        with resource_lock:
            if resource_name in resource_data:
                return True
            else:
                return False
