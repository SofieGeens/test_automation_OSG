# -*- coding: utf-8 -*-
"""
@author: Michiel

This module contains the base class for our data types, using pickle for the
serialization and de-serialization.
"""
import pickle

from codeBRT.datatypes.interface import IDataType


class UndefinedDataType(TypeError):
    """Error when trying to use an undefined data type."""


class PickleBase(IDataType):
    """ Base class for serialization using pickle. """

    @classmethod
    def check_data_type(cls, data_type):
        """

        Args:
            data_type: A data type which needs to be checked to be valid.

        Returns: The unchanged data type.

        Raises:
            InvalidDataType: If data_type is not a valid data type.

        """

        if isinstance(data_type, IDataType):
            return data_type
        else:
            raise UndefinedDataType('Invalid data type {}'.format(data_type))

    def raw_is_type_of(self, obj):
        try:
            pickle.dumps(obj)
            return True
        except TypeError:
            return False

    def is_type_of(self, obj):
        if obj is None:
            return True
        else:
            return self.raw_is_type_of(obj)

    def serialize(self, obj):
        return pickle.dumps(obj)

    def deserialize(self, byte_repr):
        return pickle.loads(byte_repr)
