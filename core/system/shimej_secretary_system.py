# Copyright 2024 hd company
# Authors: Hyeongjun Jeon

import copy

from core.shimeji.base.base_shimeji_entity import EntityProperty


class ShimejiSecretarySystem:

    def __init__(self, entity: EntityProperty):
        print('=========시메지 월드=========')
        self.entity_property = copy.deepcopy(entity)

        print(self.entity_property.entity_properties)

    def activate(self):
        pass
