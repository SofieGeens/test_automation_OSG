# -*- coding: utf-8 -*-
"""
This is the minimal viable implementation requirement of a general EventType.
Adding types/subtypes afterwards should never break any behavior.
"""

from enum import Enum


class GenericType(Enum):
    def __new__(cls, type_id, subtype=None):
        obj = object().__new__(cls)
        obj._value_ = type_id
        obj.subtype = subtype

        if obj.subtype is not None:
            for sub_obj in obj.subtype:
                sub_obj.supertype = obj
        return obj

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def _missing_(cls, value, default=0):
        if not cls.has_value(default):
            return super()._missing_(value)
        return cls(default)


class SystemEventSubtype(GenericType):
    """
    System subtypes represent specific parameters of the measurement.
    Such as store events, that determine when the measurement started and ended.
    """
    UNDEFINED = 0
    STORE = 1


class HypnogramEventSubtype(GenericType):
    UNDEFINED = 0
    INVALID = -1
    WAKE = 2
    REM = 201
    N1 = 301
    N2 = 302
    N3 = 303
    N4 = 304


class SaturationEventSubtype(GenericType):
    UNDEFINED = 0
    DIP = 1


class EegEventSubtype(GenericType):
    UNDEFINED = 0
    K_COMPLEX = 1
    SPINDLE = 2


class EogEventSubtype(GenericType):
    UNDEFINED = 0
    REM = 1
    SEM = 2


class SoundEventSubtype(GenericType):
    UNDEFINED = 0
    SNORING = 1


class BodypositionEventSubtype(GenericType):
    UNDEFINED = 0
    LEFT_SIDE = 1
    RIGHT_SIDE = 2
    BACK = 3
    BELLY = 4
    STANDING_UP = 5
    HEAD_DOWN = 6

    @classmethod
    def valids(cls):
        return cls.lying_positions() + cls.standing_positions()

    @classmethod
    def lying_positions(cls):
        return [cls.LEFT_SIDE, cls.RIGHT_SIDE, cls.BACK, cls.BELLY]

    @classmethod
    def standing_positions(cls):
        return [cls.STANDING_UP]


class SleepEventSubtype(GenericType):
    UNDEFINED = 0
    LIGHTS_OUT = 1


class EventType(GenericType):
    UNDEFINED = 0
    SYSTEM = 1, SystemEventSubtype
    NOTE = 64
    HYPNOGRAM = 128, HypnogramEventSubtype
    SATURATION = 130, SaturationEventSubtype
    EEG = 133, EegEventSubtype
    EOG = 134, EogEventSubtype
    AROUSAL = 135
    SOUND = 136, SoundEventSubtype
    BODYPOSITION = 137, BodypositionEventSubtype
    SLEEP = 139, SleepEventSubtype


class EmgChannelSubtype(GenericType):
    """Don't merge subtype CHIN_ENVELOPPE to CHIN"""
    UNDEFINED = 0
    CHIN = 19


class Spo2ChannelSubtype(GenericType):
    UNDEFINED = 0
    HEART_RATE = 10
    SAO2 = 12


class SoundChannelSubtype(GenericType):
    UNDEFINED = 0
    CANNULA_SNORE = 32
    CPAP_SNORE = 31
    RAW = 22
    ENVELOPE = 23


class ChannelType(GenericType):
    UNDEFINED = 0
    EEG = 1
    EMG = 2, EmgChannelSubtype
    ECG = 3
    EOG = 4
    SPO2 = 6, Spo2ChannelSubtype
    SOUND = 7, SoundChannelSubtype
