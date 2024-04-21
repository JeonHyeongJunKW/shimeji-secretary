# Copyright 2024 hd company
# Authors: Hyeongjun Jeon

from core.shimeji.base.base_shimeji_entity import BaseShimejiEntity


class BaseShimejiBuilder:

    def __init__(self):
        pass

    def make_entity(self, entity_property):
        is_valid = entity_property.check_validation()  # builder duty
        if not is_valid:
            return None

        return BaseShimejiEntity(entity_property)
