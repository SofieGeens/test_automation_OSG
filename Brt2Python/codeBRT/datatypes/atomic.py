# -*- coding: utf-8 -*-
"""
@author: Steven

This module contains definitions for the basic (atomic) python types.
"""
import warnings

import numpy as np

from codeBRT.datatypes.base import PickleBase
from codeBRT.datatypes.interface import IDataType


def _basic_type(btype):
    """
    Generates a data type for a given basic python type (btype).
    Serialization and deserialization is provided by pickle.

    The attribute _type of this data type returns the basic python type it is
    defined from, in order to support numpy type hierarchy for arrays and
    dataframes.

    Currently supported types:
    - int
    - bool
    - float
    - complex
    - str
    """

    def basic_is_instance(self, obj):
        """

        Args:
            self: The data type itself.
            obj: An object that is to be tested.

        Returns: Whether this object belongs to this data type.

        """
        return isinstance(obj, btype)

    def basic_np_subtype(self, np_dtype):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=FutureWarning)
            np_types = {int: np.integer, float: np.floating, bool: np.bool,
                        complex: np.complexfloating, str: np.str}
            if not np.issubdtype(np_dtype, np_types[btype]):
                return False
            else:
                return True

    doc_string = "Data type for {}. See Base class for serialization and " \
                 "deserialization.".format(btype.__name__)

    return type(btype.__name__,
                (PickleBase,),
                {'raw_is_type_of': basic_is_instance,
                 '__doc__': doc_string,
                 'np_subtype': basic_np_subtype})()  # singleton type


Int = _basic_type(int)
Bool = _basic_type(bool)
Float = _basic_type(float)
Complex = _basic_type(complex)


class _StrType(IDataType):
    """
    Data type for strings. The serialization and deserialization is the standard
    utf-8 encoding.
    """

    def is_type_of(self, obj):
        return isinstance(obj, str)

    def raw_is_type_of(self, obj):
        return isinstance(obj, str)

    def serialize(self, obj):
        return bytes(obj, encoding='utf-8')

    def deserialize(self, str_repr):
        return str_repr.decode('utf-8')

    def np_subtype(self, np_dtype):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=FutureWarning)
            return np.issubdtype(np_dtype, str)


Str = _StrType()
