# Copyright 2024 hd company
# Authors: Hyeongjun Jeon

import copy

from core.drawer.main_drawer import MainDrawer
from core.shimeji.base.base_shimeji_builder import BaseShimejiBuilder
from core.shimeji.base.base_shimeji_entity import BaseEntityProperty


class ShimejiSecretarySystem:

    def __init__(self):
        print('=========시메지 월드=========')
        self.__base_builder = BaseShimejiBuilder()
        self.__main_drawer = MainDrawer()
        self.shimeji_set = []

    def activate(self):
        self.__main_drawer.activate()

    def made_shimeji(self, shimeji_property: BaseEntityProperty):
        if 'unique_type' not in shimeji_property:
            entity = self.__base_builder.make_entity(shimeji_property)
        else:
            entity = self.__base_builder.make_entity(shimeji_property)

        if entity is not None:
            self.shimeji_set.append(entity)
