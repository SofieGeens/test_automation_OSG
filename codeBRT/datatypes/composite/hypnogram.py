# -*- coding: utf-8 -*-
import io
from enum import Enum

import numpy as np

from codeBRT.datatypes.interface import IDataType


class Stage(Enum):
    """Representation of a Hypnogram's Stage."""
    WAKE = 0
    N1 = 1
    N2 = 2
    N3 = 3
    R = 4
    INVALID = 5

    @classmethod
    def valids(cls):
        return [cls.WAKE, cls.N1, cls.N2, cls.N3, cls.R]


class _hypnogram_type(IDataType):
    """
    This is a type of Array that serializes through its Stage enum value,
    rather than the full enum object.
    """
    def raw_is_type_of(self, obj):
        result = False
        if isinstance(obj, np.ndarray) and obj.ndim == 1:
            for elem in obj:
                if not isinstance(elem, Stage):
                    break
            else:
                result = True
        return result

    def is_type_of(self, obj):
        return self.raw_is_type_of(obj) or obj is None

    def serialize(self, obj):
        def get_value(stage):
            return stage.value

        get_value = np.vectorize(get_value)
        intermediate = get_value(obj)
        result = io.BytesIO()
        np.save(result, intermediate)
        return result.getvalue()

    def deserialize(self, byte_repr):
        intermediate = np.load(io.BytesIO(byte_repr))

        def create_stage(value):
            return Stage(value)

        create_stage = np.vectorize(create_stage)
        value = create_stage(intermediate)
        return value


HypnogramType = _hypnogram_type()
