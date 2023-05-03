# -*- coding: utf-8 -*-
from dataclasses import dataclass

from codeBRT.datatypes.atomic import Float, Int
from codeBRT.datatypes.composite.array import Array
from codeBRT.datatypes.composite.dataclass import DataClass


@dataclass(frozen=True)
class Signal:
    signal: Array(Float, 1)
    sampling_rate: Int


SignalType = DataClass(Signal)
