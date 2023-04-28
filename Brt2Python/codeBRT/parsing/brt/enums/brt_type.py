# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 09:41:32 2019

@author: JanA
"""

from enum import Enum


def generate_generic_type(generic_base, supervalue, subvalue):
    """Transformer for BrainRT types into generic types."""
    supertype = generic_base(supervalue)
    if supertype.subtype is not None and supertype.subtype.has_value(subvalue):
        subtype = supertype.subtype(subvalue)
    else:
        subtype = generic_base(0)
    return subtype if subtype is not generic_base(0) else supertype


def interpret_generic_type(brt_base, generic_type):
    """Transformer for generic types into BrtTypes."""
    if hasattr(generic_type, 'supertype'):
        supervalue = generic_type.supertype.value
        subvalue = generic_type.value
    else:
        supervalue = generic_type.value
        subvalue = 0
    brt_subtype = brt_base(supervalue).subtype(subvalue)
    return brt_subtype


class BrtType(Enum):
    """
    Base class for both enumerated BrtChannelType and BrtEventType, and any subtypes.
    
    Attributes:
        - value: the integer identifier used in BrainRT.
        - type_name: the given name of this type.
        - subtype: the enumerated subtype belonging to this type.
                   (None for BrtType hierarchy leafs.)
    """

    def __new__(cls, type_id, type_name, subtype=None):
        obj = object().__new__(cls)
        obj._value_ = type_id
        obj.type_name = type_name
        obj.subtype = subtype

        # Add the reflexive arrow to the subtypes, if necessary.
        if obj.subtype is not None:
            for sub_obj in obj.subtype:
                sub_obj.supertype = obj
        return obj

    @classmethod
    def has_value(cls, value):
        """Check if there is a type associated to this value."""
        return value in cls._value2member_map_

    @classmethod
    def _missing_(cls, value, default=0):
        """Catch the situation where a value is missing."""
        if not cls.has_value(default):
            return super()._missing_(value)
        return cls(default)
