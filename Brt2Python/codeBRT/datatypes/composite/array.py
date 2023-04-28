# -*- coding: utf-8 -*-
import numpy as np

from codeBRT.datatypes.base import PickleBase, UndefinedDataType


class Array(PickleBase):
    """
    Data type for (non-object) numpy arrays with specific number of dimensions.
    See Base class for serialization and deserialization.

    Attributes:
        element_type: The data type of the elements of this array.
        dimension: The amount of dimensions of this array.

    Note:
        The only allowed el_types are the atomic data types.
        This is because the type checking uses the numpy dtype hierarchy.
    """

    def __init__(self, element_type, dimension):
        self.el_type = self.check_data_type(element_type)
        self.dimension = dimension
        if not isinstance(dimension, int) or dimension <= 0:
            msg = 'The dimension of an array needs to be positive and integral.'
            raise UndefinedDataType(msg)

    def raw_is_type_of(self, obj):
        if not isinstance(obj, np.ndarray):
            return False
        elif len(obj.shape) != self.dimension and len(obj) != 0:
            return False
        else:
            return self.el_type.np_subtype(obj.dtype)

    def __eq__(self, other):
        return ((isinstance(other, Array)
                and self.el_type == other.el_type
                and self.dimension == other.dimension) or
                other.__class__ == PickleBase)

