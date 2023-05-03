# -*- coding: utf-8 -*-
from codeBRT.datatypes.base import PickleBase


class Dict(PickleBase):
    """
    Data type for dictionaries with homogeneous keys/values.
    See Base class for serialization and deserialization.

    Args:
            key_type: The type of the dictionary's keys.
            value_type: The type of the dictionary's values.
    """

    def __init__(self, key_type, value_type):
        self.key_type = self.check_data_type(key_type)
        self.value_type = self.check_data_type(value_type)

    def raw_is_type_of(self, obj):
        if not isinstance(obj, dict):
            return False
        else:
            for key, value in obj.items():
                if (not self.key_type.raw_is_type_of(key) or
                        not self.value_type.raw_is_type_of(value)):
                    return False
        return True

    def __eq__(self, other):
        return isinstance(other, Dict) and self.key_type == other.key_type and \
               self.value_type == other.value_type
