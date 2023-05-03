# -*- coding: utf-8 -*-
from codeBRT.datatypes.base import PickleBase
from codeBRT.parsing.interface.generic_type import ChannelType, EventType, \
    GenericType


class EventMetaTypeClass(PickleBase):
    """
    The class generating the datatype for all defined generic EventTypes (and
    EventSubTypes).

    See Base class for serialization and deserialization.
    """

    def raw_is_type_of(self, obj):
        if not isinstance(obj, GenericType):
            return False
        else:
            try:
                obj = obj.supertype
            except AttributeError:
                pass

            return isinstance(obj, EventType)


class ChannelMetaTypeClass(PickleBase):
    """
    The class generating the datatype for all defined generic ChannelTypes (and
    ChannelSubTypes).

    See Base class for serialization and deserialization.
    """

    def raw_is_type_of(self, obj):
        if not isinstance(obj, GenericType):
            return False
        else:
            try:
                obj = obj.supertype
            except AttributeError:
                pass

            return isinstance(obj, ChannelType)


# These singletons are the actual data types, which are to be called outside.
EventMetaType = EventMetaTypeClass()
ChannelMetaType = ChannelMetaTypeClass()
