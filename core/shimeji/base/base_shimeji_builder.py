# Copyright 2024 hd company
# Authors: Hyeongjun Jeon

from core.shimeji.base.base_shimeji_entity import BaseEntityProperty, BaseShimejiEntity


class BaseShimejiBuilder:

    def __init__(self):
        pass

    def make_entity(self, entity_property: dict):
        is_valid = BaseEntityProperty.check_validation(entity_property)  # builder duty
        if not is_valid:
            return None

        return BaseShimejiEntity(entity_property)
