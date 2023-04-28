# -*- coding: utf-8 -*-
from dataclasses import fields

from codeBRT.datatypes.base import PickleBase, UndefinedDataType
from codeBRT.datatypes.interface import IDataType


class DataClass(PickleBase):
    """
    Transforms a dataclass into its associated data type.
    See Base class for serialization and deserialization.

    Attributes:
        data_cls: Dataclass to be converted into a data type.

    Raises:
        ValueError: If the type annotations are not valid data types.
    """
    def __init__(self, data_cls):
        self.data_cls = data_cls
        for field in fields(self.data_cls):
            if not isinstance(field.type, IDataType):
                raise UndefinedDataType('Invalid data type {}'.format(field.type))

    def raw_is_type_of(self, obj):
        """
        Return whether a given object (obj) is an instance of this dataclass,
        where the type annotations are obeyed.
        """
        if not isinstance(obj, self.data_cls):
            return False
        for field in fields(self.data_cls):
            if not field.type.raw_is_type_of(getattr(obj, field.name)):
                return False
        return True

    def __eq__(self, other):
        return isinstance(other, DataClass) and self.data_cls == other.data_cls
