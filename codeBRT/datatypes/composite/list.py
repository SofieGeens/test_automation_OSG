# -*- coding: utf-8 -*-
from codeBRT.datatypes.base import PickleBase


class List(PickleBase):
    """
    Data type for homogeneous python lists.
    See Base class for serialization and deserialization.

    Attributes:
        element_type: The data type of the elements of this list.
    """

    def __init__(self, element_type):
        self.el_type = self.check_data_type(element_type)

    def raw_is_type_of(self, obj):
        if not isinstance(obj, list):
            return False
        else:
            for el in obj:
                if not self.el_type.raw_is_type_of(el):
                    return False
        return True

    def __eq__(self, other):
        return isinstance(other, List) and self.el_type == other.el_type
