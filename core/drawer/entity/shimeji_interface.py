# Copyright 2024 hd company
# Authors: Hyeongjun Jeon

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget


class ShimejiInterface(QWidget):

    def __init__(self, resource_path: str):
        super().__init__()
        uic.loadUi(resource_path, self)
        self.setWindowFlag(Qt.FramelessWindowHint)
