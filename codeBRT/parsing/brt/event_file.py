# -*- coding: utf-8 -*-
import os
from io import BytesIO

import numpy as np
import pandas as pd

from codeBRT.parsing.brt.components.event import BrtEvent
from codeBRT.parsing.brt.components.header import EventBlockHeader
from codeBRT.parsing.brt.enums.brt_type import generate_generic_type
from codeBRT.parsing.brt.enums.event_type import BrtEventType, SystemSubtype
from codeBRT.parsing.interface.generic_type import EventType


class MissingEventFile(FileNotFoundError):
    """Raised when attempting to read an event file where none exists."""


class BrtEventFileReader:
    """
    Reader for a single BrainRT file.

    Attributes:
        path: Path of the BrainRT Event file
        events: dataframe of all events
    """
    # TODO: add manual/automatic to event data.
    file_header_size = 98

    pure_event_block = 1
    event_data_block = 2
    end_of_events_block = 3

    time_scale = 1000000

    fields = ["event_type", "event_subtype", "time", "duration",
              "data_size", "data_offset", "flags", "raw_data"]

    def __init__(self, path: str):
        if not os.path.exists(path):
            raise MissingEventFile(f"There is no event file at {path}.")
        self.path = path
        self.events = None

    def read_events(self, event_type: BrtEventType = None):
        """
        Generate the event list belonging to the specified event type.
        This also correctly locates all events.

        Args:
            event_type: BrainRT event type of the events to be read.
        Returns:
            Event list containing the events read.
        """
        self.events = {}
        if event_type is not None:
            if event_type != BrtEventType.SYSTEM:
                self._read_events(BrtEventType.SYSTEM.value)
            self._read_events(event_type.value)
        else:
            self._read_events()
        self.events = pd.concat(list(self.events.values()), ignore_index=True)
        self.adjust_time_scale()
        if event_type is not None:
            self.events = self.events[self.events.event_type == event_type.value]

        def extract_generic_event_type(row):
            event_type = row.event_type
            event_subtype = row.event_subtype
            return generate_generic_type(EventType, event_type, event_subtype)

        generic_types = self.events.apply(
            extract_generic_event_type,
            axis=1
        )
        self.events["manual"] = ((self.events['flags'] % 8) // 4 != 1) | ((self.events['flags'] % 4)//2 == 1)
        self.events = self.events[(self.events['flags'] % 16) // 8 != 1]
        self.events.drop(["event_subtype", "data_size", "data_offset", "flags"], axis=1, inplace=True)
        if len(self.events) != 0:
            self.events.event_type = generic_types
        return self.events

    def _read_events(self, event_type_id: int = None):
        """
        Read the events of the given event type.

        Args:
            event_type_id: Id number of the event type to be read.
        """
        with open(self.path, 'rb') as handle:
            handle.seek(self.file_header_size)
            block_type = None
            while block_type != self.end_of_events_block:
                header = EventBlockHeader.parse_from(handle)
                block_type = header.block_type
                if (event_type_id is not None) and \
                   (header.event_type_id != event_type_id):
                    handle.seek(header.offset + header.block_size)
                    continue
                if header.block_type == self.pure_event_block:
                    self._read_event_block(header, handle)
                elif header.block_type == self.event_data_block:
                    self._read_data_block(header, handle)
            self._read_sequential_events(header, handle, event_type_id)

    def _read_event_block(self, header: EventBlockHeader, handle: BytesIO):
        """
        Read a single event block containing a list of events.

        Args:
            header: header of the event block.
            handle: handle of the event file being read.
        """
        n_events = header.block_size // BrtEvent.size()
        block_events = np.ndarray((n_events, len(self.fields)), dtype=object)
        for i in range(n_events):
            # Note to self: don't touch this loop!!!
            event = BrtEvent.parse_from(handle)
            block_events[i] = [event.event_type_id, event.event_subtype_id,
                               event.time, event.duration, event.data_size,
                               event.info, event.flags, b'']
        block_df = pd.DataFrame(block_events, columns=self.fields)
        self.events[header.event_type_id] = block_df

    def _read_data_block(self, header: EventBlockHeader, handle: BytesIO):
        """
        Reads all data in a single datablock, containing data of one subtype.
        Args:
            header: event block header of the event block
            handle: handle of the event file being read

        """
        if header.block_size == 0:
            return
        content = handle.read(header.block_size)
        event_df = self.events[header.event_type_id]
        subevents_df = event_df.loc[event_df.event_subtype ==
                                    header.event_subtype_id]

        def select_data(row):
            return content[row.data_offset:][:row.data_size]

        data_series = subevents_df.apply(select_data, axis=1)
        event_df.raw_data = data_series

    def _read_sequential_events(self, header: EventBlockHeader, handle: BytesIO,
                                event_type_id: int = None):
        """
        Read the sequential events at the end of the file.
        These should not exist in a file which was correctly closed.

        Args:
            header: header denoting the end of the events in this file
            handle: handle of the event file being read
            event_type_id: If not None, only read the events of this type_id
        """
        handle.seek(header.offset)
        _event = handle.read(BrtEvent.size())
        event_rows = []
        while len(_event) == BrtEvent.size():
            event = BrtEvent.parse(_event)
            data = handle.read(event.data_size)
            if event_type_id is None or event.event_type_id == event_type_id:
                event_rows += [[event.event_type_id, event.event_subtype_id,
                               event.time, event.duration, event.data_size,
                               event.info, event.flags, data]]
            _event = handle.read(BrtEvent.size())

        if event_type_id is not None:
            events_df = self.events[event_type_id]
            df_rows = pd.DataFrame(event_rows, columns=events_df.columns)
            self.events[event_type_id] = events_df.append(df_rows, ignore_index=True)
        else:
            for event_type in set([i[0] for i in event_rows]):
                events_df = self.events[event_type]
                rows_event_type = [i for i in event_rows if i[0]==event_type]
                df_rows = pd.DataFrame(rows_event_type, columns=events_df.columns)
                self.events[event_type] = events_df.append(df_rows, ignore_index=True)

    def adjust_time_scale(self):
        """
        Changes the time and duration of all events to relative time.
        This is a scale expressed in seconds, starting at the (original) first
        store rounded to the nearest realtime second.
        """
        sys_events = self.events.loc[
            self.events.event_type == BrtEventType.SYSTEM.value]
        orig_span_id = SystemSubtype.ORIGINAL_SIGNAL_SPAN.value
        store_subtype = orig_span_id \
            if orig_span_id in sys_events.event_subtype.values \
            else SystemSubtype.STORE.value
        # determine the store events
        store_events = sys_events.loc[sys_events.event_subtype == store_subtype]
        scale = self.time_scale
        offset = min(store_events.time)
        offset = offset - offset % scale

        # apply first time offset of the event of the given stores
        self.events.time = (self.events.time - offset) / scale
        self.events.duration = self.events.duration / scale

