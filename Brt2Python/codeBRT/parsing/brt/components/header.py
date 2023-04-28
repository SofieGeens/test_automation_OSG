# -*- coding: utf-8 -*-
from dataclasses import dataclass

from codeBRT.parsing.brt.components.base import Component
from codeBRT.parsing.brt.enums.brt_type import BrtType
from codeBRT.parsing.brt.enums.event_type import BrtEventType


@dataclass(frozen=True)
class Header(Component):
    """
    Dataclass representation of a BrainRT header block.
    This contains a general description of another block in this file.

    Attributes:
        block_type: identifier for the type of block to be expected
        block_offset: position of the block associated to this header
        block_size: size of the block associated to this header
        block_flags: some indications about the block's general behavior

        type_string: "unsigned integer, long long, long long, unsigned integer"
    """
    block_type: int
    block_offset: int
    block_size: int
    block_flags: int

    type_string = '=IqqI'


@dataclass(frozen=True)
class Count(Component):
    """
    Component of a file which describes any kind of count, or list length.

    Attributes:
        count: number of objects described by this component

        type_string: "unsigned integer"
    """
    count: int

    type_string = '=I'


@dataclass(frozen=True)
class EventBlockHeader(Component):
    """
    Headers governing the way an event file is written.

    Properties:
        event_type: the BrainRT type of event stored in this block
        event_subtype: The BrainRT subtype stored in this block, only nonzero if
            this is an event data block.

    Attributes:
        block_type: the type id of this event block header
        block_size: Size of the data stored in this block of data
        offset: start of the block this header describes, usually immediately
            after the header.

        type_string: 'unsigned short, unsigned short, unsigned short,
            unsigned integer, long long'
    """
    block_type: int
    event_type_id: int
    event_subtype_id: int
    block_size: int
    offset: int

    @property
    def event_type(self) -> BrtEventType:
        return BrtEventType(self.event_type_id)

    @property
    def event_subtype(self) -> BrtType:
        return self.event_type.subtype(self.event_subtype_id)

    type_string = '=HHHIq'
