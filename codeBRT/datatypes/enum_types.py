# -*- coding: utf-8 -*-
from codeBRT.datatypes.interface import IDataType


class EnumType(IDataType):
    """
    DataType class for Enums.
    Use this as InputAttribute(datatype=EnumType(SomeEnum)).
    Note that "None" is not an element of any of these types.

    Attributes:
        enum_cls: the enum class to which this enum type is linked.
    """
    def __init__(self, enum_cls):
        self.enum_cls = enum_cls

        if any(obj.value<0 or obj.value>255 for obj in enum_cls):
            min_val = min([obj.value for obj in enum_cls])
            max_val = max([obj.value for obj in enum_cls])
            byte_len = max(1, (max_val - min_val).bit_length()//4)

            def long_serialize(obj):
                "Serialization replacement, in case the fast option fails."
                value = obj.value - min_val
                return value.to_bytes(byte_len, byteorder='big')
            self.serialize = long_serialize

            def long_deserialize(byte_repr):
                "Deserialization replacement, in case the fast option fails."
                value = int.from_bytes(byte_repr, byteorder='big')
                return self.enum_cls(value + min_val)
            self.deserialize = long_deserialize

    def is_type_of(self, obj):
        return isinstance(obj, self.enum_cls)

    def raw_is_type_of(self, obj):
        return isinstance(obj, self.enum_cls)

    def serialize(self, obj):
        return bytes([obj.value])

    def deserialize(self, byte_repr):
        return self.enum_cls(int.from_bytes(byte_repr, byteorder='big'))

    def __eq__(self, other):
        return self.enum_cls is other.enum_cls
