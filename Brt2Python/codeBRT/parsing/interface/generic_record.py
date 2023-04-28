# -*- coding: utf-8 -*-
from dataclasses import dataclass

from codeBRT.datatypes.atomic import Bool, Float, Int, Str
from codeBRT.datatypes.composite.array import Array
from codeBRT.datatypes.composite.list import List
from codeBRT.datatypes.meta_type import ChannelMetaType, EventMetaType


@dataclass(frozen=True)
class MeasurementInfo:
    age: Float
    stores: Array(Float, 2)
    date: List(Int)
    birth_date: List(Int)


@dataclass(frozen=True)
class SignalSegment:
    start: Float
    data: Array(Float, 1)
    sampling_rate: Int


@dataclass(frozen=True)
class Channel:
    name: Str
    sampling_rate: Int
    channel_type: ChannelMetaType
    maximum_value: Float = float('inf')
    minimum_value: Float = - float('inf')


@dataclass(frozen=True)
class Event:
    event_type: EventMetaType
    time: Float
    duration: Float
    manual: Bool
