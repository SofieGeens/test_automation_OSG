# -*- coding: utf-8 -*-
import itertools as it

from codeBRT.datatypes.base import PickleBase, UndefinedDataType


class Tuple(PickleBase):
    """
    Data type for python tuple of fixed size.
    See Base class for serialization and deserialization.

    Attributes:
        element_type: The data type of the elements of this tuple.
        size: The number of elements in this tuple.
    """

    def __init__(self, element_types, size=None):
        if isinstance(element_types, (list, tuple)):
            self.el_type = [self.check_data_type(el_type) for el_type in element_types]
            if size is None:
                size = len(self.el_type)
        else:
            self.el_type = [self.check_data_type(element_types)]
        if size < 0 or not isinstance(size, int):
            msg = "Tuples should have a positive integral size."
            raise UndefinedDataType(msg)
        self.size = size

    def raw_is_type_of(self, obj):
        if not isinstance(obj, tuple):
            return False
        elif not len(obj) == self.size:
            return False
        else:
            for el, el_type in zip(obj, it.cycle(self.el_type)):
                if not el_type.raw_is_type_of(el):
                    return False
        return True

    def __eq__(self, other):
        if not (isinstance(other, Tuple) and
                self.size == other.size):
            return False
        for i, left, right in zip(range(self.size),
                                  it.cycle(self.el_type),
                                  it.cycle(other.el_type)):
            if left != right:
                return False
        return True
