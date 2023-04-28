# -*- coding: utf-8 -*-
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class DataDescription:
    """Descriptions necessary to parse the signals in the given signal file."""
    sampling_rates: np.array

    transform_slopes: np.array
    transform_intercepts: np.array

    def __post_init__(self):
        *offsets, block_size = [0, *np.cumsum(self.sampling_rates)]
        object.__setattr__(self, 'offsets', offsets)  # setattr hacks "frozen"
        object.__setattr__(self, 'block_size', block_size)