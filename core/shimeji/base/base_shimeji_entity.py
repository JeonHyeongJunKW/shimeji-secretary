# Copyright 2024 hd company
# Authors: Hyeongjun Jeon


class EntityProperty:

    def __init__(self):
        self.entity_properties = []

    def add(self, name: str, animation_type: str = 'static'):
        self.entity_properties.append(
            {'name': name,
             'animation_type': animation_type})
