# -*- coding: utf-8 -*-
import datetime
import itertools
import os
import re

import numpy as np

from codeBRT.parsing.brt.enums.brt_type import interpret_generic_type
from codeBRT.parsing.brt.enums.event_type import BrtEventType
from codeBRT.parsing.brt.event_file import BrtEventFileReader, MissingEventFile
from codeBRT.parsing.brt.header import MissingHeaderFile, BrtHeaderReader
from codeBRT.parsing.brt.signal_file import BrtSignalFileReader, MissingSignalFile
from codeBRT.parsing.interface.base import InvalidExtension, IReader
from codeBRT.parsing.interface.generic_record import MeasurementInfo, \
    SignalSegment
from codeBRT.parsing.interface.generic_type import EventType


class BrtMeasurementReader(IReader):
    """
    BrainRT reader of measurements including the signal files and event files.

    Args:
        path: the location of the measurement
    Attributes:
        directory: see args.
        filename: see args.
    Properties:
        signal_files: The signal file objects belonging to this measurement.
        event_file: The event file object belonging to this measurement.
        stores: The stores of this measurement.
    """

    def __init__(self, path, event_type=None):
        if path[-8:] != "-hdr.sig":
            msg = "A Brt reader can't read measurements that don't end in " \
                  "'-hdr.sig'. Make sure the correct reader was applied to " \
                  "this measurement. "
            raise InvalidExtension(msg=msg)
        
        self.path = path

        self.event_type = event_type

        self._signal_files = None
        self._event_file = None
        self._stores = None
        self._header = None

    @property
    def header(self):
        if self._header is None:
            self._header = self._create_header()
        return self._header

    @property
    def signal_files(self):
        if self._signal_files is None:
            self._signal_files = self._create_signal_files()
        return self._signal_files

    @property
    def event_file(self):
        if self._event_file is None:
            self._event_file = self._create_event_file()
        return self._event_file

    @property
    def stores(self):
        if self._stores is None:
            self._stores = self._read_stores()
        return self._stores

    def _create_signal_files(self):
        signal_files = []
        for i in itertools.count(1):
            path = os.path.join(self.path[:-8] + f"-t{i}.sig")
            if not os.path.exists(path):
                if i == 1:
                    msg = f"There was no signal file for measurement " \
                          f"at location {self.path}. " \
                          f"This measurement may not exist."
                    raise MissingSignalFile(msg)
                break
            signal_files.append(BrtSignalFileReader(path))
        return signal_files

    def _create_event_file(self):
        path = os.path.join(self.path[:-8] + f"-evt.sig")
        if not os.path.exists(path):
            msg = f"There was no event file for measurement" \
                  f" at location {self.path}. " \
                  f"This measurement may not exist."
            raise MissingEventFile(msg)
        return BrtEventFileReader(path)

    def _read_stores(self):
        system_events = self.event_file.read_events(BrtEventType.SYSTEM)
        stores = system_events[
            system_events.event_type == EventType.SYSTEM.subtype.STORE]
        stores = np.array([stores.time.to_numpy(), stores.duration.to_numpy()],
                          dtype=float)
        return stores.T

    def _create_header(self):
        path = self.path
        if not os.path.exists(path):
            msg = f"There was no header file for measurement" \
                  f" at location {path}. " \
                  f"This measurement may not exist."
            raise MissingHeaderFile(msg)
        return BrtHeaderReader(path)

    @property
    def channel_list(self):
        """
        The channel lists of the first signal file.
        This is supposed to represent the channel lists of the other signal
        files as well.

        Returns:
            The Channel List describing this measurement.
        """
        first_signal_file = self.signal_files[0]
        channel_info = first_signal_file.read_channel_info()
        return channel_info

    def _read_signal(self, channel_index: int):
        """
        Reads the entire signal belonging to a specific channel.

        Args:
            channel_index: The index of the channel to be read.

        Returns:
            A tuple of SignalSegments containing the segments of the signal,
            and the position of these segments.
        """
        data = []
        for i, signal_file in enumerate(self.signal_files):
            if len(self.stores) > i:
                signal = signal_file.read_data(channel_index)
                start = self.stores[i, 0]
                sampling_rate = signal_file.data_description.sampling_rates[channel_index]
                segment = SignalSegment(start, signal, int(sampling_rate))
                data.append(segment)
        return list(data)

    def read_data(self, channel_type=None):
        data = {}
        for i, channel in enumerate(self.channel_list):

            if channel_type is None:
                criterion = True
            elif hasattr(channel_type, 'supertype'):
                criterion = channel_type == channel.channel_type
            else:
                if hasattr(channel.channel_type, 'supertype'):
                    criterion = channel.channel_type.supertype == channel_type
                else:
                    criterion = channel.channel_type == channel_type

            if criterion:
                data[channel.name] = self._read_signal(i)
        return data

    def read_events(self, event_type=None):
        """
        Reads the event list belonging to the specific (generic) event type.

        Args:
            event_type: Generic event type, if any.

        Returns:
            event list compatible with the IEventList functionality.
        """
        if event_type is not None:
            brt_subtype = interpret_generic_type(BrtEventType, event_type)
            brt_type = brt_subtype.supertype
        else:
            brt_type = None
        event_list = self.event_file.read_events(brt_type)
        return event_list.drop('raw_data', axis=1)

    def get_age(self):
        """
        Calculates the patient age from info in the header. Since date of birth
        is an approximation to provide anonymity, only an approximation of the
        age can be plausibly made.

        Returns: Approximation of patient age, in years, rounded to one digit
            after the decimal point

        """
        measurement_date = self.get_date()
        birth_date = self.get_birth_date()
        if measurement_date is None or birth_date is None:
            return -1.0
        age = datetime.date(*measurement_date) - datetime.date(*birth_date)
        age = age.days / 365.25
        if 0 <= age <= 150:
            return round(age, 1)
        else:
            return -1.0

    def get_date(self):
        """
        Returns: The start date of the measurement, read from the
             header and converted to [year, month, day].
        """
        date_string = self.header.info['MeasurementInfo']['StartDateAndTime']
        if date_string is None:
            return None

        date_string = re.split('T', date_string)[0]
        date_list = [int(ymd) for ymd in re.split('-', date_string)]
        return date_list

    def get_birth_date(self):
        """
         Returns: The approximate birth date of the patient, read from the
             header and converted to [year, month, day].

         Note: This birth date is not exact to provide patient anonymity.

         """
        date_string = self.header.info['PatientInfo']['DateOfBirth']
        if date_string is None:
            return None

        date_list = [int(ymd) for ymd in re.split('-', date_string)]
        return date_list

    @property
    def measurement_info(self):
        """
        Measurement info.

        Returns:
            MeasurementInfo stub, compatible with IMeasurementInfo.
        """
        age = self.get_age()
        date = self.get_date()
        birth_date = self.get_birth_date()
        measurement_info = MeasurementInfo(age=age, stores=self.stores,
                                           date=date, birth_date=birth_date)
        return measurement_info
