# Copyright 2024 Hyeongjun Jeon
# Authors: Hyeongjun Jeon
import os


def get_resource_path(relative_path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


if __name__ == '__main__':
    path = get_resource_path('test.txt')
    print(path)
