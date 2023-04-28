# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class InvalidExtension(IOError):
    """Raised when reading a file with an mismatched extension."""
    pass


class IReader(ABC):
    """
    An interface for reading any kind of file format.

    Arguments:
        path: path of the measurement
    Attributes:
        channel_list: list of all channels in the measurement
        event_list: dataframe containing the events in the measurement
        data: dictionary mapping the channel names to their signals
        measurement_info: general information about the measurement
    """

    @property
    @abstractmethod
    def channel_list(self):
        """list of all channels in the measurement"""

    @abstractmethod
    def read_events(self, event_type):
        """
        Reads the events of the specified event type.

        Args:
            event_type: event_type of the events to be read.

        Returns:
            dataframe containing the events in the measurement
        """

    @abstractmethod
    def read_data(self, channel_type):
        """
        read the data belonging to the specified channel type.

        Args:
            channel_type: channel_type of the data to be read

        Returns:
            Dictionary mapping the channel names to their signals.
        """

    @property
    @abstractmethod
    def measurement_info(self):
        """general information about the measurement"""
