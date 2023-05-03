# -*- coding: utf-8 -*-
import os
from typing import List

import numpy as np

from codeBRT.parsing.brt.components.channel import BrtChannel
from codeBRT.parsing.brt.components.data_description import DataDescription
from codeBRT.parsing.brt.components.header import Count, Header
from codeBRT.parsing.interface.generic_record import Channel


class IllegalOverwrite(RuntimeError):
    """Raised when attempting to overwrite a property with valuable data."""


class MissingSignalFile(FileNotFoundError):
    """Raised when attempting to read a signal file that does not exist."""


class BrtSignalFileReader:
    """
    Signal File Reader

    Args:
        path: a complete path of a BrainRT file to be parsed

    Attributes:
        file_header_size: fixed size of the file header of any signal file
        number_of_headers: fixed number of headers in any signal file
        type_of_samples_description: block type of a samples description block
        type_of_samples_data: block type of a samples data block
        path: see args

    Properties:
        headers: list of headers present in this file
    """
    file_header_size = 98
    number_of_headers = 64

    type_of_samples_description = 1179648
    type_of_samples_data = 1245184

    @property
    def headers(self) -> List[Header]:
        """ list of headers present in this file """
        if self._headers is None:
            self._headers = self._read_headers()
        return self._headers

    def __init__(self, path: str):
        if not os.path.exists(path):
            raise MissingSignalFile(f"No signal file at location {path}.")
        self.path = path

        self._headers = None
        self.data_description = None

    def read_channel_info(self) -> List[Channel]:
        """
        Reads the channel info in the given signal file.

        Returns:
            Channel Info compatible with IChannelList
        """
        header = next(header for header in self.headers
                      if header.block_type == self.type_of_samples_description)
        with open(self.path, 'rb') as handle:
            handle.seek(header.block_offset + Header.size())
            n_channels = Count.parse_from(handle).count

            channel_list = [None]*n_channels
            sampling_rates = np.empty(n_channels, dtype=int)
            slopes = np.empty(n_channels, dtype=float)
            intercepts = np.empty(n_channels, dtype=float)
            for index in range(n_channels):
                channel = BrtChannel.parse_from(handle)
                sampling_rates[index] = channel.sampling_rate
                slopes[index] = channel.mf_PV
                intercepts[index] = channel.af_PV
                channel_list[index] = Channel(
                    name=channel.name,
                    sampling_rate=channel.sampling_rate,
                    channel_type=channel.generic_type
                )
        self.data_description = DataDescription(
            sampling_rates=sampling_rates,
            transform_slopes=slopes,
            transform_intercepts=intercepts
        )

        return channel_list

    def read_data(self, index: int) -> np.ndarray:
        """
        Read the data belonging to the channel specified by its index.

        Args:
            index: Channel at the specified index.

        Returns:
            Signal data from the relevant channel.
        """
        if self.data_description is None:
            self.read_channel_info()
        fs = self.data_description.sampling_rates[index]
        offset = self.data_description.offsets[index]

        header = next(header for header in self.headers
                      if header.block_type == self.type_of_samples_data)
        with open(self.path, 'rb') as handle:
            handle.seek(header.block_offset)
            content = handle.read()

        data = np.frombuffer(content, np.int16)
        data = data.reshape((-1, self.data_description.block_size))
        data = data[:, offset: (offset + fs)]

        signal = data.flatten()
        signal = (signal * self.data_description.transform_slopes[index] +
                  self.data_description.transform_intercepts[index])
        return signal

    def _read_headers(self) -> List[Header]:
        """
        Reads the headers of this signal file.

        Returns:
            List of header objects.
        """
        headers = []
        with open(self.path, 'rb') as handle:
            handle.seek(self.file_header_size)
            for _ in range(self.number_of_headers):
                header = Header.parse_from(handle)
                headers.append(header)
        return headers
