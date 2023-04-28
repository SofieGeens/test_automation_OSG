# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from codeBRT.datatypes.atomic import Bool, Float
from codeBRT.datatypes.base import PickleBase, UndefinedDataType
from codeBRT.datatypes.meta_type import EventMetaType
from utils.deep_equals import deep_equals


class DataFrame(PickleBase):
    """
    Data type for pandas DataFrames.
    See Base class for serialization and deserialization.

    Attributes:
        column_types_dict: Dictionary with respectively the column labels and
            the types of these columns as keys and values.

    Note:
        As for Array, it is attempted to do type checking by using the numpy
        dtype hierarchy, using the innate dtype of pandas Series. If this dtype
        is not atomic, the Series gets iterated over to ascertain correctness.
    """

    def __init__(self, column_types_dict):
        if not isinstance(column_types_dict, dict):
            raise UndefinedDataType(
                f'{column_types_dict} needs to be a dictionary')
        for key in column_types_dict:
            try:
                self.check_data_type(column_types_dict[key])
            except TypeError:
                raise UndefinedDataType(
                    f'Invalid data type {column_types_dict[key]}')
            self.column_types_dict = column_types_dict

    def raw_is_type_of(self, obj):
        if not isinstance(obj, pd.DataFrame):
            return False

        elif set(self.column_types_dict.keys()) != set(obj.columns):
            return False

        elif obj.empty:
            return True

        for key in obj.columns:
            value_type = self.column_types_dict[key]

            # thorough check if dtype of the series is dtype('object')
            if obj[key].dtype == np.dtype(object):
                for el in obj[key]:
                    if not value_type.raw_is_type_of(el):
                        return False
            else:
                if not value_type.np_subtype(obj[key].dtype):
                    return False
        return True

    def __eq__(self, other):
        if not isinstance(other, DataFrame):
            return False

        return deep_equals(self.column_types_dict, other.column_types_dict)


EventListType = DataFrame({'time': Float, 'duration': Float, 'manual': Bool,
                           'event_type': EventMetaType})
