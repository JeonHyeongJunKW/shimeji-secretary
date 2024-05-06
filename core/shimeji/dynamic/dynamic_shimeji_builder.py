# Copyright 2024 Hyeongjun Jeon
# Authors: Hyeongjun Jeon

from core.shimeji.random.random_shimeji_builder import RandomShimejiBuilder
from core.shimeji.dynamic.dynamic_shimeji_entity import DynamicEntityProperty, DynamicShimejiEntity


class DynamicShimejiBuilder(RandomShimejiBuilder):

    def __init__(self):
        super(RandomShimejiBuilder, self).__init__()

    def check_validation(self, entity_property: DynamicEntityProperty) -> bool:
        result = super().check_validation(entity_property)
        if not result:
            return False
        return True

    def make_entity(self, entity_property):
        is_valid = self.check_validation(entity_property)
        if not is_valid:
            return None

        return DynamicShimejiEntity(entity_property)
