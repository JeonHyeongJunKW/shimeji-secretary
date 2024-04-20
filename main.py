# Copyright 2024 hd company
# Authors: Hyeongjun Jeon

from core.shimeji.base.base_shimeji_entity import BaseEntityProperty
from core.system.shimeji_secretary_system import ShimejiSecretarySystem

if __name__ == '__main__':
    secretary_system = ShimejiSecretarySystem()
    secretary_system.activate()