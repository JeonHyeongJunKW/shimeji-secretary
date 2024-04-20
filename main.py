# Copyright 2024 hd company
# Authors: Hyeongjun Jeon

from core.shimeji.base.base_shimeji_entity import EntityProperty
from core.system.shimej_secretary_system import ShimejiSecretarySystem

if __name__ == '__main__':
    entity_property = EntityProperty()
    entity_property.add('유동길')

    secretary_system = ShimejiSecretarySystem(entity_property)
