# -*- coding: utf-8 -*-
from dataclasses import dataclass

from codeBRT.parsing.brt.components.base import Component
from codeBRT.parsing.brt.enums.brt_type import BrtType, generate_generic_type
from codeBRT.parsing.brt.enums.event_type import BrtEventType
from codeBRT.parsing.interface.generic_type import EventType, GenericType


@dataclass(frozen=True)
class BrtEvent(Component):
    """Representation of a BrainRT event as written in an event file."""
    event_type_id: int
    event_subtype_id: int
    time: int
    duration: int
    flags: int
    owned_by_id: int
    owner_id: int
    info: int
    data_size: int
    reference: int
    originator: int
    offset: int

    @property
    def event_type(self) -> BrtEventType:
        return BrtEventType(self.event_type_id)

    @property
    def event_subtype(self) -> BrtType:
        return self.event_type.subtype(self.event_subtype_id)

    @property
    def is_manual(self) -> bool:
        return ((self.flags % 8)//4 != 1) or ((self.flags % 4)//2 == 1)

    @property
    def generic_type(self) -> GenericType:
        return generate_generic_type(
            EventType,
            self.event_type_id,
            self.event_subtype_id)

    type_string = '=HHqqHHHIIHIq'
