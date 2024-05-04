# Copyright 2024 Hyeongjun Jeon
# Authors: Hyeongjun Jeon

from core.shimeji.base.base_shimeji_builder import BaseShimejiBuilder
from core.shimeji.random.random_shimeji_entity import RandomEntityProperty, RandomShimejiEntity


class RandomShimejiBuilder(BaseShimejiBuilder):

    def __init__(self):
        super(RandomShimejiBuilder, self).__init__()

    def check_validation(self, entity_property: RandomEntityProperty) -> bool:
        result = super().check_validation(entity_property)
        if not result:
            return False
        if entity_property.get('use_random_seed') is None:
            entity_name = entity_property.get('name')
            print('There is no random seed option in {0}'.format(entity_name))
            return False
        return True

    def make_entity(self, entity_property):
        is_valid = self.check_validation(entity_property)
        if not is_valid:
            return None

        return RandomShimejiEntity(entity_property)
