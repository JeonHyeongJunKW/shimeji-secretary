# Copyright 2024 hd company
# Authors: Hyeongjun Jeon

from core.shimeji.base.base_shimeji_builder import BaseShimejiBuilder
from core.shimeji.random.random_shimeji_entity import RandomShimejiEntity


class RandomShimejiBuilder(BaseShimejiBuilder):

    def __init__(self):
        super(RandomShimejiBuilder, self).__init__()

    def make_entity(self, entity_property):
        is_valid = entity_property.check_validation()  # builder duty
        if not is_valid:
            return None

        return RandomShimejiEntity(entity_property)
